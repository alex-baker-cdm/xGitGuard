#!/usr/bin/env python3
"""
Network connectivity test for OpenTelemetry integration
Tests port availability and basic network connectivity
"""

import socket
import sys

def test_port_availability(host, port):
    """Test if a port is available for binding"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error testing port {port}: {e}")
        return False

def test_network_connectivity():
    """Test basic network connectivity"""
    try:
        import requests
        response = requests.get('https://httpbin.org/get', timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Network connectivity test failed: {e}")
        return False

def main():
    print("=== OpenTelemetry Network Access Test ===")
    
    collector_ports = [4317, 4318]
    print("\n1. Testing collector port availability:")
    
    for port in collector_ports:
        if test_port_availability('localhost', port):
            print(f"   Port {port}: IN USE (may need to stop existing collector)")
        else:
            print(f"   Port {port}: AVAILABLE ✓")
    
    print("\n2. Testing network connectivity:")
    if test_network_connectivity():
        print("   Internet connectivity: OK ✓")
    else:
        print("   Internet connectivity: FAILED ✗")
    
    print("\n3. Testing socket binding on collector ports:")
    for port in collector_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('localhost', port))
            sock.close()
            print(f"   Can bind to port {port}: YES ✓")
        except Exception as e:
            print(f"   Can bind to port {port}: NO - {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
