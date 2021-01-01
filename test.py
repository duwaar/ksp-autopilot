import krpc

print("Trying to connect to kRPC server...")
conn = krpc.connect(
        address='127.0.0.1',
        rpc_port=50000,
        stream_port=50001)
print("Server running with kRPC version {}.".format(conn.krpc.get_status().version))

