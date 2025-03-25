# before running, pip install these packages:
# > pip install wiliot-deployment-tools binascii

from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient, ExtendedPlatformClient, EdgeClient, BridgeThroughGatewayAction, GatewayType
import binascii
import json
import time
import random
import argparse
from datetime import datetime
from colorama import init

# Initialize colorama (necessary for Windows)
init(autoreset=True)

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

api_key = ''
owner_id = ''
gw_id = '' 
cloud = ''  # 'gcp' or 'aws'  ('us-central1' if cloud=='gcp' else 'us-east-2')  'us-east-2' 
env =  ''  # 'prod' or 'test'
region = ''
desired_app_version = '' 
retries = 100
shuffle_src_brgs = True
api_ver  = '0A'
rssi_threshold = -60
src_brg_id_list =[]
dst_brg_id_list =[]

src_brg2brg_list = []
dst_list = []
dst_brg2brg_list = []
dst_gw2brg_list = []

gw_type = ""
latest_bl = 18
minimal_bl = 12



 #Get Token using API Key
e = []
ec = []



def cur_time():
    current_time = datetime.now()
    
    # Extract only the time components (hours, minutes, seconds)
    time_components = current_time.strftime('%H:%M:%S')
    return time_components


def time_diff_sec(prev_time):
    current_epoch_time = int(time.time())
    return int(current_epoch_time - prev_time/1000)

def is_brg_relevat_as_brg2brg_src_brg(e, brg_id, gw_id):
    is_relevat = False
    brg_dict = e.get_bridge(brg_id)
    brg_id = brg_dict['id']   
            
    for conn in brg_dict['connections']:
        if  'rssi' in conn and conn['rssi'] > -68 and conn['gatewayId'] == gw_id :
            is_relevat = True 
    
    return is_relevat 




def get_brg_modules(e, brg_id, gw_id):
    sq_id =  random.randint(10, 99) 
    packet = (f'1E16C6FC0000ED0709{sq_id}{brg_id}03FE00000000000000000000000000')
    e.send_packet_through_gw(gateway_id=gw_id, raw_packet=packet, is_ota=False, repetitions='3')

def is_brg_ota_secceeded(e, brg_id, desired_app_version, desired_brg_zone):
    upgrade_succeedded = 0   
    brg_test = e.get_bridge(brg_id)
    brg_zone = None
    brg_zone_name = None
    if 'zone' in brg_test:          
        brg_zone = brg_test['zone'] 
        brg_zone_name = brg_zone['name']

    if(brg_test['version'] == desired_app_version):
       upgrade_succeedded = 1
       if(brg_test['bootloaderVersion'] == latest_bl and brg_id not in src_brg_id_list and is_brg_relevat_as_brg2brg_src_brg(e, brg_id, gw_id)):
          src_brg_id_list.append(brg_id)
          upgrade_succeedded = 2
       
    return upgrade_succeedded



def check_brg2brg_ota(update_bl, gw_type, brg2brg_only):

    wait_time = 0    
    if GatewayType.WIFI == gw_type or GatewayType.FANSTEL_LAN_V0 == gw_type or brg2brg_only :
        wait_time = 220 if update_bl else 120
    elif  GatewayType.RIGADO == gw_type :
        wait_time = 180 if update_bl else 100    
    else:
        wait_time = 550 if update_bl else 340

    print(BLUE +"[{}] Waiting {} seconds for the OTA upgrade to complete".format(cur_time(), wait_time) + RESET)
    time.sleep(wait_time) 

           
def brg2brg_ota(e,ec, undorted_src_brg2brg_list, dst_brg2brg_list):
    src_brg2brg_list = sorted(undorted_src_brg2brg_list, key=lambda x: x["rssi"], reverse=True)
    random.shuffle(dst_brg2brg_list)
    for src_brg, dst_brg in zip(src_brg2brg_list, dst_brg2brg_list):
        sq_id =  random.randint(10, 99)
        reboot_packet = f'1E16AFFD0000ED0300{sq_id}{dst_brg["id"]}010000000000000000000000000000'
        packet = (f'1E16AFFD0000ED08{api_ver}{sq_id+1}{src_brg["id"]}02{dst_brg["id"]}0000000000000000')            
        e.send_packet_through_gw(gateway_id=src_brg["gw"], raw_packet=reboot_packet, is_ota=False, tx_max_duration=300, repetitions=5) 
        print(MAGENTA2 +"[{}] Brg2Brg OTA Brg Id {} to Bridge {} (via GW {} with RSSI {})".format(cur_time(), src_brg["id"], dst_brg["id"], src_brg["gw"], src_brg["rssi"]) + RESET)   
        e.send_packet_through_gw(gateway_id=src_brg["gw"], raw_packet=packet, is_ota=False, tx_max_duration = 300, repetitions=5)
        time.sleep(1)  
     

def gw2brg_ota(e,ec, undorted_dst_gw2brg_list, desired_app_version, cloud, env,region):
    used_gw_id = set()
    dst_gw2brg_list = sorted(undorted_dst_gw2brg_list, key=lambda x: x["rssi"], reverse=True)

    for dst_gw2brg in dst_gw2brg_list:
        gw_id = dst_gw2brg["gw"]
        brg_id = dst_gw2brg["id"]
        desired_brg_type = dst_gw2brg["boardType"]

        if(gw_id in used_gw_id):
            continue
        else:
            used_gw_id.add(gw_id)


       # sq_id =  random.randint(10, 99) 
       # print(BLUE +"\n[{}] About to disable PL mode for bridge id {}".format(cur_time(), brg_id) + RESET)   
       # packet_disable_pl = ( f'1E16AFFD0000ED07{api_ver}{sq_id}{brg_id}0B0000000000000000000000000000') 
       # e.send_packet_through_gw(gateway_id=gw_id, raw_packet=packet_disable_pl, is_ota=False, tx_max_duration=300, repetitions=5) 
       # time.sleep(2) 

        sq_id =  random.randint(10, 99)         
        update_bl = True if (dst_gw2brg["bootloaderVersion"] < latest_bl) else False
        print(MAGENTA +"[{}] Gw2Brg OTA Brg Id {} (version {}) to version {} via GW {} with RSSI {}".format(cur_time(), brg_id, dst_gw2brg["version"],desired_app_version, gw_id, dst_gw2brg["rssi"]) + RESET)          
        imageDirUrl = (f'https://api.{region}.{env}.wiliot.cloud/v1/bridge/type/{desired_brg_type}/version/{desired_app_version}/binary/') if cloud !='gcp' else  (f'https://api.{region}.{env}.gcp.wiliot.cloud/v1/bridge/type/{desired_brg_type}/version/{desired_app_version}/binary/')
        
        payload = {
            "action": 1, # Upgrade bridge
            "gatewayId": gw_id, # optional. for the c2c data flows    
            # // Advertise parameters:
            "imageDirUrl":imageDirUrl,
            "upgradeBlSd": update_bl,
            "txPacket": ( f'1E16AFFD0000ED0300{sq_id}{brg_id}010000000000000000000000000000'),
            "txMaxDurationMs": 750,
            "txMaxRetries" : 8,
            "bridgeId": brg_id
        }                 
        e.send_custom_message_to_gateway(gateway_id=gw_id, custom_message=payload) 
        time.sleep(1)  


def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    
    parser.add_argument('--owner_id', '-oi', required=True, type=str, help='Owner Id')
    parser.add_argument('--api_key', '-ak', required=True, type=str, help='API Key')
    parser.add_argument('--gateway', '-gw', required=False, default=None,type=str, help='Gw to use for OTA')
    parser.add_argument('--cloud', '-cl', required=False, default='aws', choices=['aws', 'gcp'], type=str, help='Cloud Enviorment')
    parser.add_argument('--enviorment', '-env', required=False, default='prod', choices=['prod', 'test', 'dev'], type=str, help='Production/Test Enviorment')
    parser.add_argument('--brg_id', '-bi', required=True, type=str, help='Bridge Id') 
    parser.add_argument('--brg_ver', '-bv', required=True, type=str, help='Bridge Version')
    parser.add_argument('--rssi_threshold', '-rt', required=False, default=-60, type=int, help='rssi threshold')
    parser.add_argument('--app_only', '-ao', required=False, default=False , type=bool, help='Application Only(no Bootloader upgrade)')
    
    args = parser.parse_args()
    print(args.__dict__)
    
    owner_id = args.owner_id
    api_key = args.api_key
    gw_id = None
    all_brgs = []
    cloud = args.cloud
    env = args.enviorment
    first_brg_id = args.brg_id
    desired_app_version = args.brg_ver
    global desired_brg_location
    global desired_brg_zone
    global src_brg_id_list
    rssi_threshold = args.rssi_threshold
    app_only = args.app_only
    global shuffle_src_brgs
    global src_brg_id_list
    global brg_location_name
    shuffle_src_brgs = True
    src_brg_id_list = [] 
    desired_brg_zone = None
    brg_location_name = None
    desired_brg_location = None
    desired_brg_type = None
    location_id = None
    last_cycle_sec = 0
     
    region = 'us-central1' if cloud == 'gcp' else 'us-east-2'

     #Get Token using API Key
    e = ExtendedEdgeClient(api_key, owner_id, env ,region, cloud)   
    ec = EdgeClient(api_key, owner_id, env ,region, cloud)   
    first_brg_dict = ec.get_bridge(first_brg_id)        
    
    if 'location' in first_brg_dict: 
        location = first_brg_dict['location']          
        location_id = location['id'] 
        desired_brg_location = location['name']
    else:
        print(RED +"\n[{}] Bridge {} has no location id - aborting ...".format(cur_time(),first_brg_id) + RESET)  
        exit
            
    if 'zone' in first_brg_dict: 
        zone_dict = first_brg_dict['zone']          
        desired_brg_zone = zone_dict['name']
        print(BLUE +"\n[{}] zone {} ".format(cur_time(), desired_brg_zone) + RESET)   

    desired_brg_type =  first_brg_dict["boardType"]  
    
    for number in range(retries):
        
        # To avoid to many API calls we should wait at 60 seconds between cycles
        cur_time_sec = int(time.time())
        if cur_time_sec - last_cycle_sec < 60:
            last_cycle_sec = cur_time_sec
            wait_time = 300
            print(YELLOW +"[{}] Waiting {} second(s) before starting a new cycle".format(cur_time(), wait_time) + RESET)  
            time.sleep(wait_time)
        else:
            last_cycle_sec = cur_time_sec   
    

        #all_brgs_in_location = ec.get_bridges( online=True, params={'locationId': location_id, 'search_query':'4.2.117' })
        all_brgs_in_location = ec.get_bridges( online=True, params={'locationId': location_id})
        print(BLUE +"\n[{}] There are {} online bridges at location {}".format(cur_time(), len(all_brgs_in_location), desired_brg_location) + RESET) 
        src_brg2brg_list.clear()
        dst_brg2brg_list.clear()
        dst_gw2brg_list.clear()           
        for brg_dict in all_brgs_in_location:
            best_gw_rssi = -90 
            best_gw_rssi_time = 0                     
            brg_id = brg_dict['id']  
            if brg_dict['owned'] != True:
                continue
            
            for conn in brg_dict['connections']:               
                #if 'rssi' in conn and e.check_gw_online([conn['gatewayId']]):
                if 'rssi' in conn and conn['rssi'] < 0:
                   # print(CYAN +"\n[{}] GW {} received data from Brg {} with RSSI {} (Measured {} seconds ago)".format(cur_time(), conn['gatewayId'], brg_id, conn['rssi'], time_diff_sec(conn['rssiUpdatedAt'])) + RESET)
                    if conn['rssi'] > best_gw_rssi and  conn['rssi'] < 0 and time_diff_sec(conn['rssiUpdatedAt'])<1800:                    
                        gw_id = conn['gatewayId']
                        best_gw_rssi = conn['rssi']
                        best_gw_rssi_time = conn['rssiUpdatedAt'] 
            if gw_id == None:
                print(RED +"\n[{} No GW was available for upgrading bridge {} ({}) at location {}".format(cur_time(), brg_id, brg_dict["version"], desired_brg_location) + RESET) 
                continue 
            else:
                color = GREEN if (brg_dict["version"] == desired_app_version) else YELLOW 
                print(color +"[{}] Brg Id {} (version {}), GW Id {}, GW-Brg Rssi {} messured {} seconds ago".format(cur_time(),brg_id,brg_dict["version"],gw_id, best_gw_rssi, time_diff_sec(best_gw_rssi_time)) + RESET)     


            boardType = brg_dict['boardType'] 
            brg_bl = brg_dict['bootloaderVersion'] 
            brg_app_version = brg_dict['version']
            if 'location' in brg_dict:
                location_dict = brg_dict['location']          
                brg_location = location_dict['name']
            else:
                brg_location = None  

            brg_item = {"id": brg_id, "gw": gw_id, "rssi": best_gw_rssi, "bootloaderVersion" : brg_dict['bootloaderVersion'],"version": brg_dict['version'] , "location" : brg_location, "boardType" : boardType}

            if(brg_item['version'] == desired_app_version and brg_item['bootloaderVersion'] == latest_bl and brg_item['boardType'] == desired_brg_type):
                src_brg2brg_list.append(brg_item) 
            else:                  
                if(brg_item["rssi"] < rssi_threshold and brg_item['version'] != desired_app_version): 
                    dst_brg2brg_list.append(brg_item) 
                else:
                    dst_gw2brg_list.append(brg_item) 



        brg2brg_only = False
        update_bl = False
        gw_type = GatewayType.ERM
        if(len(src_brg2brg_list) and len(dst_brg2brg_list)):
            brg2brg_ota(e,ec, src_brg2brg_list, dst_brg2brg_list)
            brg2brg_only = True
            
        if len(dst_gw2brg_list):
            gw2brg_ota(e,ec, dst_gw2brg_list,desired_app_version, cloud, env, region)
            brg2brg_only = False
            gw_type = e.get_gateway_type(dst_gw2brg_list[0]["gw"])
            update_bl = True if (dst_gw2brg_list[0]["bootloaderVersion"] < latest_bl) else False 
      
        if(len(dst_gw2brg_list) or brg2brg_only):                
            check_brg2brg_ota(update_bl, gw_type, brg2brg_only)
        
        print(BLUE + "[{}] Ended {} cycle(s) of trying to upgrade ".format(cur_time(),number)+ RESET)
        
        if(len(dst_gw2brg_list) == 0  and  len(dst_brg2brg_list) == 0):
            break     
            
    print(BLUE + "[{}] Bridge Upgrade Process for Bridges on loaction {} is completed".format(cur_time(), location["name"])+ RESET)



if __name__ == "__main__":
    main()


