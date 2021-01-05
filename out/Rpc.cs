import lostsouls.net.lostsocket.lostsouls.net.kumo.structs.ClientHandshake;
import lostsouls.net.lostsocket.lostsouls.net.kumo.structs.Status;
import lostsouls.net.lostsocket.lostsouls.net.kumo.structs.LoginData;
import lostsouls.net.lostsocket.lostsouls.net.kumo.structs.Complex;
import lostsouls.net.lostsocket.lostsouls.net.kumo.structs.HasId;
import lostsouls.net.lostsocket.lostsouls.net.kumo.structs.SpawnData;
import lostsouls.net.lostsocket.lostsouls.net.kumo.structs.Movement;
import net.kaminari.IAckCallback;
import net.kaminari.IBroadcaster;
import net.kaminari.IBroadcastOperation;
import net.kaminari.Packet;
public class Rpc
{
    public static void sendHandshake(ProtocolQueues pq, ClientHandshake data, IAckCallback callback)
    {
        pq.sendReliable(Opcodes.opcodeHandshake, data, callback);
    }
    public static void sendHandshake(ProtocolQueues pq, ClientHandshake data)
    {
        pq.sendReliable(Opcodes.opcodeHandshake, data);
    }
    public static void broadcastHandshake(IBroadcaster<ProtocolQueues> broadcaster, ClientHandshake data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeHandshake, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void broadcastHandshake(IBroadcaster<ProtocolQueues> broadcaster, ClientHandshake data)
    {
        Packet packet = Packet.make(Opcodes.opcodeHandshake);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void broadcastHandshakeSingle(IBroadcaster<ProtocolQueues> broadcaster, ClientHandshake data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeHandshake, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void broadcastHandshakeSingle(IBroadcaster<ProtocolQueues> broadcaster, ClientHandshake data)
    {
        Packet packet = Packet.make(Opcodes.opcodeHandshake);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void sendLogin(ProtocolQueues pq, LoginData data, IAckCallback callback)
    {
        pq.sendReliable(Opcodes.opcodeLogin, data, callback);
    }
    public static void sendLogin(ProtocolQueues pq, LoginData data)
    {
        pq.sendReliable(Opcodes.opcodeLogin, data);
    }
    public static void broadcastLogin(IBroadcaster<ProtocolQueues> broadcaster, LoginData data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeLogin, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void broadcastLogin(IBroadcaster<ProtocolQueues> broadcaster, LoginData data)
    {
        Packet packet = Packet.make(Opcodes.opcodeLogin);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void broadcastLoginSingle(IBroadcaster<ProtocolQueues> broadcaster, LoginData data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeLogin, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void broadcastLoginSingle(IBroadcaster<ProtocolQueues> broadcaster, LoginData data)
    {
        Packet packet = Packet.make(Opcodes.opcodeLogin);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendReliable(packet);
            }
        });
    }
    public static void sendMove(ProtocolQueues pq, Movement data, IAckCallback callback)
    {
        pq.sendOrdered(Opcodes.opcodeMove, data, callback);
    }
    public static void sendMove(ProtocolQueues pq, Movement data)
    {
        pq.sendOrdered(Opcodes.opcodeMove, data);
    }
    public static void broadcastMove(IBroadcaster<ProtocolQueues> broadcaster, Movement data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendOrdered(packet);
            }
        });
    }
    public static void broadcastMove(IBroadcaster<ProtocolQueues> broadcaster, Movement data)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendOrdered(packet);
            }
        });
    }
    public static void broadcastMoveSingle(IBroadcaster<ProtocolQueues> broadcaster, Movement data, IAckCallback callback)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove, callback);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendOrdered(packet);
            }
        });
    }
    public static void broadcastMoveSingle(IBroadcaster<ProtocolQueues> broadcaster, Movement data)
    {
        Packet packet = Packet.make(Opcodes.opcodeMove);
        data.pack(Marshal.instance, packet);
        broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {
            public void onCandidate(ProtocolQueues pq) {
                pq.sendOrdered(packet);
            }
        });
    }
}

