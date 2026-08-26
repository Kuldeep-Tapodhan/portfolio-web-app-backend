import ipaddress
import logging
import time
import traceback

logger = logging.getLogger('api.request')

class RequestLoggingMiddleware:
    """
    Middleware to log every incoming HTTP request to the backend APIs,
    detecting and formatting both IPv4 and IPv6 client IP addresses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Process request
        response = self.get_response(request)

        duration = (time.time() - start_time) * 1000  # Convert to milliseconds

        user = getattr(request, 'user', None)
        user_str = str(user) if user and user.is_authenticated else 'Anonymous'
        ip_info = self.get_client_ip_info(request)

        status_code = response.status_code
        log_msg = f"[{ip_info}] [{request.method}] {request.get_full_path()} -> {status_code} ({duration:.2f}ms) | User: {user_str}"

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
        Returns a formatted string like 'IPv4: 172.20.0.1' or 'IPv6: 2001:db8::1' or 'IPv4: 1.2.3.4 | IPv6: 2001:db8::1'.
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
            # Handle IPv4-mapped IPv6 addresses (e.g. ::ffff:192.168.1.1)
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
