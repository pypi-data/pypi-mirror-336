from .pyruvate import serve, FileWrapper  # noqa: F401


def serve_paste(app, global_conf, **kw):
    num_headers = int(kw.get('max_number_headers', 32))
    async_logging = bool(kw.get('async_logging', 'True') != 'False')
    chunked_transfer = bool(kw.get('chunked_transfer', 'False') == 'True')
    reuse_count = int(kw.get('max_reuse_count', 0))
    keepalive_timeout = int(kw.get('keepalive_timeout', 60))
    qmon_warn_threshold = int(
        kw['qmon_warn_threshold']) if 'qmon_warn_threshold' in kw else None
    send_timeout = int(kw.get('send_timeout', 60))
    serve(
        app,
        kw.get('socket'),
        int(kw['workers']),
        max_number_headers=num_headers,
        async_logging=async_logging,
        chunked_transfer=chunked_transfer,
        max_reuse_count=reuse_count,
        keepalive_timeout=keepalive_timeout,
        qmon_warn_threshold=qmon_warn_threshold,
        send_timeout=send_timeout)
    return 0
