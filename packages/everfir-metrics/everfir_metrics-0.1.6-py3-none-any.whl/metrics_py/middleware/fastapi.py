import time
from typing import Callable, List
import fastapi
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import logger_py.logger as logger

from metrics_py import metrics
from metrics_py.metrics_manager.metric_info import (
    MetricInfo,
    MetricType,
    exponential_buckets,
)


class FastAPIMiddleware(BaseHTTPMiddleware):
    # 默认的指标定义
    DEFAULT_METRICS: List[MetricInfo] = [
        MetricInfo(
            metric_type=MetricType.COUNTER,
            name="requests_counter",
            help="Total number of requests",
            labels=["method", "path", "status"],
        ),
        MetricInfo(
            metric_type=MetricType.HISTOGRAM,
            name="request_duration",
            help="HTTP request duration in milliseconds",
            labels=["method", "path", "status"],
            buckets=exponential_buckets(
                start=50, factor=1.85, count=12  #  [50ms -> 60s]
            ),
        ),
    ]

    def __init__(self, app: fastapi.FastAPI):
        super().__init__(app)
        for metric in self.DEFAULT_METRICS:
            metrics.register(metric)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求并收集指标"""
        # 记录开始时间
        start_time = time.time()

        try:
            # 处理请求
            response = await call_next(request)

            # 计算请求处理时间（毫秒）
            duration_ms = (time.time() - start_time) * 1000

            # 标签
            labels = {
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
            }

            # 记录请求计数
            metrics.report(
                metric_name="requests_counter",
                value=1,
                labels=labels,
            )

            # 记录请求延迟
            metrics.report(
                metric_name="request_duration",
                value=duration_ms,
                labels=labels,
            )

            return response
        except Exception as e:
            logger.Warn({}, msg=f"Error processing request: {e}")
            raise
