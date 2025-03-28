from __future__ import annotations
import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from serper_wrapper import SerperClient
from serper_wrapper.exceptions import SerperAPIError


class TestSerperClient(unittest.TestCase):
    """SerperClient测试类"""
    
    def setUp(self):
        """测试前的设置"""
        self.api_key = os.getenv("SERPER_API_KEY")
        self.temp_dir = tempfile.mkdtemp()
        self.client = SerperClient(
            api_key=self.api_key,
            cache_type="disk",
            cache_dir=self.temp_dir,
            max_cache_size_mb=10,
            cache_expiration=3600
        )
        
        # 模拟API返回的响应
        self.mock_response = {
            "searchParameters": {
                "q": "test query",
                "gl": "us",
                "hl": "en",
                "num": 10,
                "page": 1
            },
            "organic": [
                {
                    "title": "Test Result 1",
                    "link": "https://example.com/1",
                    "snippet": "This is a test result 1"
                },
                {
                    "title": "Test Result 2",
                    "link": "https://example.com/2",
                    "snippet": "This is a test result 2"
                }
            ]
        }
        
        # 测试的source参数
        self.source = "test_source"
    
    def tearDown(self):
        """测试后的清理"""
        # 清理临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('requests.post')
    def test_search(self, mock_post):
        """测试搜索方法"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_post.return_value = mock_response
        
        # 执行搜索
        result = self.client.search("test query", source=self.source)
        
        # 验证结果
        self.assertEqual(result, self.mock_response)
        self.assertEqual(len(result["organic"]), 2)
        self.assertEqual(result["organic"][0]["title"], "Test Result 1")
        
        # 验证API调用
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["headers"]["X-API-KEY"], self.api_key)
        self.assertEqual(json.loads(kwargs["data"])["q"], "test query")
    
    @patch('requests.post')
    def test_search_with_params(self, mock_post):
        """测试带参数的搜索方法"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_post.return_value = mock_response
        
        # 执行带参数的搜索
        result = self.client.search(
            query="test query",
            source=self.source,
            country="jp",
            language="ja",
            time_period="1w",
            num_results=20,
            page=2
        )
        
        # 验证API调用参数
        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs["data"])
        self.assertEqual(payload["q"], "test query")
        self.assertEqual(payload["gl"], "jp")
        self.assertEqual(payload["hl"], "ja")
        self.assertEqual(payload["tbs"], "qdr:w")
        self.assertEqual(payload["num"], 20)
        self.assertEqual(payload["page"], 2)
    
    @patch('requests.post')
    def test_api_error(self, mock_post):
        """测试API错误处理"""
        # 设置模拟错误响应
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response
        
        # 验证错误抛出
        with self.assertRaises(SerperAPIError):
            self.client.search("test query", source=self.source)
    
    @patch('requests.post')
    def test_cache(self, mock_post):
        """测试缓存功能"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_post.return_value = mock_response
        
        # 第一次搜索（应该调用API）
        self.client.search("test query", source=self.source)
        self.assertEqual(mock_post.call_count, 1)
        
        # 第二次相同搜索（应该使用缓存，不调用API）
        self.client.search("test query", source=self.source)
        self.assertEqual(mock_post.call_count, 1)  # 调用次数应该没有增加
        
        # 清空缓存
        self.client.clear_cache()
        
        # 第三次搜索（应该再次调用API）
        self.client.search("test query", source=self.source)
        self.assertEqual(mock_post.call_count, 2)
    
    @patch('requests.post')
    def test_custom_search(self, mock_post):
        """测试自定义搜索"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_post.return_value = mock_response
        
        # 自定义搜索参数
        custom_payload = {
            "q": "test query",
            "gl": "uk",
            "hl": "en-gb",
            "num": 5,
            "tbs": "qdr:d"
        }
        
        # 执行自定义搜索
        result = self.client.custom_search(custom_payload, source=self.source)
        
        # 验证API调用参数
        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs["data"])
        self.assertEqual(payload, custom_payload)

    @patch('serper_wrapper.client.SerperClient._push_metrics')
    @patch('requests.post')
    def test_metrics(self, mock_post, mock_push_metrics):
        """测试指标功能"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_post.return_value = mock_response
        
        # 创建带指标的客户端
        metrics_client = SerperClient(
            api_key="test_api_key",
            metrics_gateway="localhost:9091",
            metrics_job="test_job"
        )
        
        # 确保指标初始化
        self.assertTrue(metrics_client.metrics_initialized)
        
        # 执行搜索
        metrics_client.search("test query", source=self.source)
        
        # 验证_push_metrics方法被调用
        mock_push_metrics.assert_called()


if __name__ == '__main__':
    unittest.main() 