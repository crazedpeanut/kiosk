import kiosk_client_network

def not_json_recv(self, data):
    print("test", data)

command_list = {"notjson":not_json_recv}

client_thrd = kiosk_client_network.start_client(command_list)
