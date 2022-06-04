import shodan
import sys

YOUR_API_KEY_HERE=''
api_call=shodan.Shodan(YOUR_API_KEY_HERE)
# query='org:microsoft'
query = ' '.join(sys.argv[1:])


if len(sys.argv) == 1:
        print('Usage: %s <search query>' % sys.argv[0])
        sys.exit(1)

def getting_total_ips():
    try:
        total_ips=api_call.count(query)
        return total_ips['total']
    except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)
    

def page(total_ips):
    if total_ips<100:
        pages=1
    else:
        pages=(total_ips//100)+1
    return pages

def remove_duplicate_ip(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def getting_ip_list(total_ips):
    ip_list=[]
    if total_ips==0:
        pass
    else:
        try:
            number_of_page=page(total_ips)
            for pages in range(number_of_page):
                result = api_call.search(query,page=pages)
                for service in result['matches']:
                    ip_list.append(service['ip_str'])   
        except Exception as e:
            print('Error: %s' % e)
    return ip_list


def writing_in_file(unique_IPs):
    with open(r'result.txt', 'w') as fp:
        for ip in unique_IPs:
            fp.write("%s\n" % ip)
    return None


if __name__ == '__main__':
    total_ips=getting_total_ips()
    print("Total IPs found: "+str(total_ips))
    ip_list=getting_ip_list(total_ips)
    unique_IPs=remove_duplicate_ip(ip_list)
    writing_in_file(unique_IPs)
    print("Total unique IPs added in result.txt: "+str(len(unique_IPs)))