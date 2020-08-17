class Rpc
{
    public void sendMove(ProtocolQueues pq, Movement data, IAckCallback callback)
    {
        pq.sendOrdered(Marshal.instance, Opcodes.opcodeMove, data, callback);
    }
    public void sendMove(ProtocolQueues pq, Movement data)
    {
        pq.sendOrdered(Marshal.instance, Opcodes.opcodeMove, data);
    }
    public void broadcastMove(IBroadcaster broadcaster, Movement data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation {
            void onCandidate(ProtocolQueue pq) {;
                pq.sendOrdered(packet);
            });
        });
    }
    public void broadcastMove(IBroadcaster broadcaster, Movement data)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation {
            void onCandidate(ProtocolQueue pq) {;
                pq.sendOrdered(packet);
            });
        });
    }
    public void broadcastMoveSingle(IBroadcaster broadcaster, Movement data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation {
            void onCandidate(ProtocolQueue pq) {;
                pq.sendOrdered(packet);
            });
        });
    }
    public void broadcastMoveSingle(IBroadcaster broadcaster, Movement data)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation {
            void onCandidate(ProtocolQueue pq) {;
                pq.sendOrdered(packet);
            });
        });
    }
}

