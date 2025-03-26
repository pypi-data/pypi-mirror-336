import pytest
from fastapi.testclient import TestClient
from api import app
import json
from datetime import datetime

client = TestClient(app)

def test_health_check():
    """测试健康检查接口"""
    response = client.post(
        "/mcp/v1/execute",
        json={
            "request_id": "test-001",
            "version": "1.0.0",
            "action": "health_check",
            "parameters": {}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "timestamp" in data["data"]

def test_optimize_listing_success():
    """测试listing优化接口 - 成功场景"""
    response = client.post(
        "/mcp/v1/execute",
        json={
            "request_id": "test-002",
            "version": "1.0.0",
            "action": "optimize_listing",
            "parameters": {
                "asin": "B0CKWM4F9Q",
                "marketplace_id": "ATVPDKIKX0DER"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "versions" in data["data"]
    assert "analysis" in data["data"]

def test_optimize_listing_invalid_asin():
    """测试listing优化接口 - 无效ASIN"""
    response = client.post(
        "/mcp/v1/execute",
        json={
            "request_id": "test-003",
            "version": "1.0.0",
            "action": "optimize_listing",
            "parameters": {
                "asin": "INVALID_ASIN",
                "marketplace_id": "ATVPDKIKX0DER"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "ASIN_NOT_FOUND"

def test_invalid_action():
    """测试无效的操作"""
    response = client.post(
        "/mcp/v1/execute",
        json={
            "request_id": "test-004",
            "version": "1.0.0",
            "action": "invalid_action",
            "parameters": {}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "INVALID_ACTION"

def test_version_mismatch():
    """测试版本不匹配"""
    response = client.post(
        "/mcp/v1/execute",
        json={
            "request_id": "test-005",
            "version": "2.0.0",
            "action": "health_check",
            "parameters": {}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "VERSION_MISMATCH"

def test_rate_limit():
    """测试速率限制"""
    # 发送超过限制的请求
    for i in range(61):
        response = client.post(
            "/mcp/v1/execute",
            json={
                "request_id": f"test-{i}",
                "version": "1.0.0",
                "action": "health_check",
                "parameters": {}
            }
        )
        if i == 60:
            assert response.status_code == 429
            data = response.json()
            assert data["detail"]["error"] == "RATE_LIMIT_EXCEEDED"
        else:
            assert response.status_code == 200 