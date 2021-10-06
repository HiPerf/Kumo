using System;
namespace Kumo
{
    public class Unsafe
    {
        public static void sendCharacterCreated(ProtocolQueues pq, CharacterSelection data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeCharacterCreated, data, callback);
        }
        public static void sendCharacterCreated(ProtocolQueues pq, CharacterSelection data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeCharacterCreated, data);
        }
        public static void broadcastCharacterCreated(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterCreated, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharacterCreated(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterCreated);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharacterCreatedSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterCreated, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharacterCreatedSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterCreated);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendHandshakeResponse(ProtocolQueues pq, Status data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeHandshakeResponse, data, callback);
        }
        public static void sendHandshakeResponse(ProtocolQueues pq, Status data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeHandshakeResponse, data);
        }
        public static void broadcastHandshakeResponse(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeHandshakeResponse, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastHandshakeResponse(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeHandshakeResponse);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastHandshakeResponseSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeHandshakeResponse, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastHandshakeResponseSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeHandshakeResponse);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendLoginResponse(ProtocolQueues pq, StatusEx data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeLoginResponse, data, callback);
        }
        public static void sendLoginResponse(ProtocolQueues pq, StatusEx data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeLoginResponse, data);
        }
        public static void broadcastLoginResponse(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginResponse, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastLoginResponse(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginResponse);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastLoginResponseSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginResponse, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastLoginResponseSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginResponse);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendCharactersList(ProtocolQueues pq, CharactersListData data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeCharactersList, data, callback);
        }
        public static void sendCharactersList(ProtocolQueues pq, CharactersListData data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeCharactersList, data);
        }
        public static void broadcastCharactersList(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharactersList, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharactersList(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharactersList);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharactersListSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharactersList, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharactersListSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharactersList);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendCharacterInformation(ProtocolQueues pq, Character data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeCharacterInformation, data, callback);
        }
        public static void sendCharacterInformation(ProtocolQueues pq, Character data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeCharacterInformation, data);
        }
        public static void broadcastCharacterInformation(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterInformation, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharacterInformation(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterInformation);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharacterInformationSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterInformation, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastCharacterInformationSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeCharacterInformation);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendLoginCharacterResult(ProtocolQueues pq, StatusEx data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeLoginCharacterResult, data, callback);
        }
        public static void sendLoginCharacterResult(ProtocolQueues pq, StatusEx data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeLoginCharacterResult, data);
        }
        public static void broadcastLoginCharacterResult(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginCharacterResult, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastLoginCharacterResult(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginCharacterResult);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastLoginCharacterResultSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginCharacterResult, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastLoginCharacterResultSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeLoginCharacterResult);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendEnterWorld(ProtocolQueues pq, Success data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeEnterWorld, data, callback);
        }
        public static void sendEnterWorld(ProtocolQueues pq, Success data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeEnterWorld, data);
        }
        public static void broadcastEnterWorld(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeEnterWorld, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastEnterWorld(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeEnterWorld);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastEnterWorldSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeEnterWorld, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastEnterWorldSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeEnterWorld);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendDoSth(ProtocolQueues pq, Complex data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeDoSth, data, callback);
        }
        public static void sendDoSth(ProtocolQueues pq, Complex data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeDoSth, data);
        }
        public static void broadcastDoSth(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDoSth, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastDoSth(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDoSth);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastDoSthSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDoSth, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastDoSthSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDoSth);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendSpawn(ProtocolQueues pq, SpawnData data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeSpawn, data, callback);
        }
        public static void sendSpawn(ProtocolQueues pq, SpawnData data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeSpawn, data);
        }
        public static void broadcastSpawn(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawn, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastSpawn(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawn);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastSpawnSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawn, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastSpawnSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawn);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendSelectedCharacterSpawnData(ProtocolQueues pq, CharacterSpawnData data, Action callback)
        {
            pq.sendReliable((ushort)Opcodes.opcodeSelectedCharacterSpawnData, data, callback);
        }
        public static void sendSelectedCharacterSpawnData(ProtocolQueues pq, CharacterSpawnData data)
        {
            pq.sendReliable((ushort)Opcodes.opcodeSelectedCharacterSpawnData, data);
        }
        public static void broadcastSelectedCharacterSpawnData(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSelectedCharacterSpawnData, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastSelectedCharacterSpawnData(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSelectedCharacterSpawnData);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastSelectedCharacterSpawnDataSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSelectedCharacterSpawnData, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void broadcastSelectedCharacterSpawnDataSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSelectedCharacterSpawnData);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendReliable(packet));
        }
        public static void sendSpawnedEntity(ProtocolQueues pq, Spawn data, Action callback)
        {
            pq.sendOrdered((ushort)Opcodes.opcodeSpawnedEntity, data, callback);
        }
        public static void sendSpawnedEntity(ProtocolQueues pq, Spawn data)
        {
            pq.sendOrdered((ushort)Opcodes.opcodeSpawnedEntity, data);
        }
        public static void broadcastSpawnedEntity(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawnedEntity, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void broadcastSpawnedEntity(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawnedEntity);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void broadcastSpawnedEntitySingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawnedEntity, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void broadcastSpawnedEntitySingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeSpawnedEntity);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void sendDespawnedEntity(ProtocolQueues pq, Despawn data, Action callback)
        {
            pq.sendOrdered((ushort)Opcodes.opcodeDespawnedEntity, data, callback);
        }
        public static void sendDespawnedEntity(ProtocolQueues pq, Despawn data)
        {
            pq.sendOrdered((ushort)Opcodes.opcodeDespawnedEntity, data);
        }
        public static void broadcastDespawnedEntity(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDespawnedEntity, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void broadcastDespawnedEntity(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDespawnedEntity);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void broadcastDespawnedEntitySingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data, Action callback)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDespawnedEntity, callback);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void broadcastDespawnedEntitySingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data)
        {
            Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcodeDespawnedEntity);
            data.pack(Marshal.instance, packet);
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendOrdered(packet));
        }
        public static void sendWorldUpdate(ProtocolQueues pq, EntityUpdate data)
        {
            pq.sendEventuallySynced((ushort)Opcodes.opcodeWorldUpdate, data);
        }
        public static void broadcastWorldUpdate(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, EntityUpdate data)
        {
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendEventuallySynced((ushort)Opcodes.opcodeWorldUpdate, data));
        }
        public static void broadcastWorldUpdateSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, EntityUpdate data)
        {
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendEventuallySynced((ushort)Opcodes.opcodeWorldUpdate, data));
        }
        public static void sendSelfWorldUpdate(ProtocolQueues pq, SelfUpdate data, Action callback)
        {
            pq.sendMostRecent((ushort)Opcodes.opcodeSelfWorldUpdate, data, callback);
        }
        public static void sendSelfWorldUpdate(ProtocolQueues pq, SelfUpdate data)
        {
            pq.sendMostRecent((ushort)Opcodes.opcodeSelfWorldUpdate, data);
        }
        public static void broadcastSelfWorldUpdate(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SelfUpdate data)
        {
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendMostRecent((ushort)Opcodes.opcodeSelfWorldUpdate, data));
        }
        public static void broadcastSelfWorldUpdateSingle(Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SelfUpdate data)
        {
            broadcaster.broadcast((ProtocolQueues pq) => pq.sendMostRecent((ushort)Opcodes.opcodeSelfWorldUpdate, data));
        }
    }

}
