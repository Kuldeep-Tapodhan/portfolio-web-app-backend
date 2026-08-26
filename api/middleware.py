import ipaddress
import json
import logging
import time
import traceback

logger = logging.getLogger('api.request')

class RequestLoggingMiddleware:
    """
    Middleware to log every incoming HTTP request to the backend APIs,
    detecting and formatting both IPv4 and IPv6 client IP addresses and payload summaries.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Capture request body for POST/PUT/PATCH before views consume it
        payload_summary = ""
        if request.method in ('POST', 'PUT', 'PATCH'):
            try:
                body = request.body.decode('utf-8') if request.body else ''
                if body:
                    data = json.loads(body)
                    if isinstance(data, dict):
                        masked_data = {
                            k: ('***' if 'password' in k.lower() or 'secret' in k.lower() else v)
                            for k, v in data.items()
                        }
                        payload_summary = f" | Payload: {json.dumps(masked_data)}"
            except Exception:
                pass

        # Process request
        response = self.get_response(request)

        duration = (time.time() - start_time) * 1000  # Convert to milliseconds

        user = getattr(request, 'user', None)
        user_str = str(user) if user and user.is_authenticated else 'Anonymous'
        ip_info = self.get_client_ip_info(request)

        status_code = response.status_code
        log_msg = f"[{ip_info}] [{request.method}] {request.get_full_path()} -> {status_code} ({duration:.2f}ms) | User: {user_str}{payload_summary}"

        if 200 <= status_code < 400:
            logger.info(f"🌐 ✅ {log_msg}")
        elif 400 <= status_code < 500:
            logger.warning(f"🌐 ⚠️ {log_msg}")
        else:
            logger.error(f"🌐 ❌ {log_msg}")

        return response

    def process_exception(self, request, exception):
        """
        Logs unhandled exceptions with IPv4/IPv6 client info and traceback.
        """
        ip_info = self.get_client_ip_info(request)
        logger.error(
            f"🌐 💥 [API EXCEPTION] [{ip_info}] [{request.method}] {request.get_full_path()}\n"
            f"Exception: {exception}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )
        return None

    def get_client_ip_info(self, request):
        """
        Extracts and categorizes IPv4 and IPv6 client IP addresses from request headers.
        """
        ip_candidates = []

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_candidates.extend([ip.strip() for ip in x_forwarded_for.split(',') if ip.strip()])

        for header in ('HTTP_X_REAL_IP', 'HTTP_CF_CONNECTING_IP', 'REMOTE_ADDR'):
            val = request.META.get(header)
            if val and val.strip():
                ip_candidates.append(val.strip())

        ipv4_list = []
        ipv6_list = []

        for raw_ip in ip_candidates:
            clean_ip = raw_ip
            if clean_ip.startswith('::ffff:'):
                clean_ip = clean_ip[7:]

            try:
                ip_obj = ipaddress.ip_address(clean_ip)
                if isinstance(ip_obj, ipaddress.IPv4Address):
                    if clean_ip not in ipv4_list:
                        ipv4_list.append(clean_ip)
                elif isinstance(ip_obj, ipaddress.IPv6Address):
                    if clean_ip not in ipv6_list:
                        ipv6_list.append(clean_ip)
            except ValueError:
                continue

        results = []
        if ipv4_list:
            results.append(f"IPv4: {', '.join(ipv4_list)}")
        if ipv6_list:
            results.append(f"IPv6: {', '.join(ipv6_list)}")

        if results:
            return " | ".join(results)
        
        return "IP: unknown"
