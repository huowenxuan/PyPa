# sudo运行

import socket
import pcap
import dpkt
import time
import urllib
import math
import os

# sniffer = pcap.pcap(name=None, promisc=True,immediate=True,timeout_ms=50)
# addr = lambda pkt, offset: '.'.join(str(pkt[i]) for i in range(offset, offset + 4))
# for ts, pkt in sniffer:
#     print('%d\tSRC %-16s\tDST %-16s' % (ts, addr(pkt, sniffer.dloff + 12), addr(pkt, sniffer.dloff + 16)))

sniffer = pcap.pcap(name=None, promisc=True, immediate=True)
for timestamp, raw_buf in sniffer:
    eth = dpkt.ethernet.Ethernet(raw_buf)

    if eth.data.__class__.__name__ == 'IP':
        ip = eth.data
        src = socket.inet_ntoa(ip.src);
        dst = socket.inet_ntoa(ip.dst);
        tcp = ip.data
        http = tcp.data

        df = bool(ip.off & dpkt.ip.IP_DF)
        mf = bool(ip.off & dpkt.ip.IP_MF)
        offset = ip.off & dpkt.ip.IP_OFFMASK
        output1 = {'time': time.strftime("%Y-%m-%d %H:%M:%S", (time.localtime(timestamp)))}
        output2 = {'src': '%d.%d.%d.%d' % tuple(list(ip.src)),
                   'dst': '%d.%d.%d.%d' % tuple(list(ip.dst))}
        output3 = {'protocal': ip.p, 'len': ip.len, 'ttl': ip.ttl}
        output4 = {'df': df, 'mf': mf, 'offset': offset, 'checksum': ip.sum}

        # if (output2['src'] == '10.130.137.119'): # 平平
        # if (output2['src'] == '10.130.136.162'): # 手机
        if (output2['src'] == '10.130.136.149'):  # 电脑
            # print(output1)
            # print(output2)
            # print(output3)
            # print(output4)
            pass

        # 有空字符串的形式，除此之外都是byte
        if isinstance(http, str):
            continue

        try:
            request = dpkt.http.Request(http)
        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
            continue
        except Exception as e:
            pass

        headers = request.headers
        host = headers.get('host')
        accept = headers.get('accept')
        user_agent = headers.get('user-agent')
        cookie = headers.get('cookie')

        full_url = host
        if request.uri and request.uri != '*':
            full_url += request.uri
        print(full_url)

    elif eth.data.__class__.__name__ == 'IP6':
        ipv6 = eth.data
        fh = dpkt.ip.IP_PROTO_FRAGMENT
        ic = dpkt.ip.IP_PROTO_ICMP6
        icmpv6 = ipv6.data

        src_ip = socket.inet_ntop(socket.AF_INET6, ipv6.src)
        dst_ip = socket.inet_ntop(socket.AF_INET6, ipv6.dst)

        # print(raw_buf)

        # print(dst_ip)
        #
        # print("==========")

        # # 有空字符串的形式，除此之外都是byte
        # if isinstance(icmpv6, str):
        #     continue
        #
        # try:
        #     request = dpkt.http.Request(icmpv6.data)
        # except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError) as e:
        #     print("error1")
        #     print(e)
        #     continue
        # except Exception as e:
        #     print("error2")
        #     print(e)
        #     pass

    else:
        # print(eth.data.__class__.__name__)
        pass
