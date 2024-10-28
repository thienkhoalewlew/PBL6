rules_to_import = [
    {
        "name": "SQL Injection",
        "description": "Detects attempts to perform SQL injection.",
        "pattern": r"(\s|^)UNION(\s|$)|(\s|^)SELECT(\s|$)|(\s|^)OR\s+1\s*=\s*1(\s|$)|(\s|^)AND\s+1\s*=\s*1(\s|$)|(\s|^)--|(\s|^)#|(\s|^)\/\*.*?\*\/|'(\s|^)OR(\s|$)'|'(\s|^)AND(\s|$)'|(\s|^)SLEEP\s*\(|(\s|^)BENCHMARK\s*\(|(\s|^)WAITFOR\s+DELAY",
        "severity": "High"
    },
    {
        "name": "XSS Attack",
        "description": "Detects most common XSS payloads.",
        "pattern": r"(<script>|<\/script>|javascript:)",
        "severity": "Medium"
    },
    {
        "name": "CSRF Attack",
        "description": "Detects CSRF vulnerabilities.",
        "pattern": r"(Forbidden \(CSRF cookie|token (missing|incorrect|not set).*?\)|CSRF verification failed)",
        "severity": "Medium"
    },
    {
        "name": "File Upload Vulnerability",
        "description": "Detects dangerous file uploads.",
        "pattern": r'"\w+\s+.*?/media/.*?(\.php|\.phtml|\.php3|\.php4|\.php5|\.phps|\.asp|\.aspx|\.jsp|\.jspx|\.exe|\.dll|\.bat|\.cmd|\.sh|\.cgi|\.pl|\.py|\.rb)"',
        "severity": "Medium"
    },
    {
        "name": "Path Traversal Attack",
        "description": "Detects path traversal attempts.",
        "pattern": r'(?:[/\\]\.\.(?:[/\\]|%2f|%5c)|%2e%2e[/\\]|%252e%252e[/\\]|/etc/|c:[/\\]windows|\.(?:log|conf|ini))',
        "severity": "High"
    }
]
