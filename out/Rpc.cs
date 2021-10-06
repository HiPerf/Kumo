using System;
namespace Kumo
{
    public class Rpc
    {
        public static void sendCharacterCreated(Kaminari.Client<ProtocolQueues> client, CharacterSelection data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendCharacterCreated(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendCharacterCreated(Kaminari.Client<ProtocolQueues> client, CharacterSelection data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendCharacterCreated(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastCharacterCreated(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterCreated(broadcaster, data, callback));
        }
        public static void broadcastCharacterCreated(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterCreated(broadcaster, data));
        }
        public static void broadcastCharacterCreatedSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterCreatedSingle(broadcaster, data, callback));
        }
        public static void broadcastCharacterCreatedSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSelection data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterCreatedSingle(broadcaster, data));
        }
        public static void sendHandshakeResponse(Kaminari.Client<ProtocolQueues> client, Status data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendHandshakeResponse(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendHandshakeResponse(Kaminari.Client<ProtocolQueues> client, Status data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendHandshakeResponse(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastHandshakeResponse(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastHandshakeResponse(broadcaster, data, callback));
        }
        public static void broadcastHandshakeResponse(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastHandshakeResponse(broadcaster, data));
        }
        public static void broadcastHandshakeResponseSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastHandshakeResponseSingle(broadcaster, data, callback));
        }
        public static void broadcastHandshakeResponseSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Status data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastHandshakeResponseSingle(broadcaster, data));
        }
        public static void sendLoginResponse(Kaminari.Client<ProtocolQueues> client, StatusEx data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendLoginResponse(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendLoginResponse(Kaminari.Client<ProtocolQueues> client, StatusEx data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendLoginResponse(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastLoginResponse(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginResponse(broadcaster, data, callback));
        }
        public static void broadcastLoginResponse(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginResponse(broadcaster, data));
        }
        public static void broadcastLoginResponseSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginResponseSingle(broadcaster, data, callback));
        }
        public static void broadcastLoginResponseSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginResponseSingle(broadcaster, data));
        }
        public static void sendCharactersList(Kaminari.Client<ProtocolQueues> client, CharactersListData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendCharactersList(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendCharactersList(Kaminari.Client<ProtocolQueues> client, CharactersListData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendCharactersList(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastCharactersList(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharactersList(broadcaster, data, callback));
        }
        public static void broadcastCharactersList(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharactersList(broadcaster, data));
        }
        public static void broadcastCharactersListSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharactersListSingle(broadcaster, data, callback));
        }
        public static void broadcastCharactersListSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharactersListData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharactersListSingle(broadcaster, data));
        }
        public static void sendCharacterInformation(Kaminari.Client<ProtocolQueues> client, Character data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendCharacterInformation(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendCharacterInformation(Kaminari.Client<ProtocolQueues> client, Character data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendCharacterInformation(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastCharacterInformation(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterInformation(broadcaster, data, callback));
        }
        public static void broadcastCharacterInformation(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterInformation(broadcaster, data));
        }
        public static void broadcastCharacterInformationSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterInformationSingle(broadcaster, data, callback));
        }
        public static void broadcastCharacterInformationSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Character data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastCharacterInformationSingle(broadcaster, data));
        }
        public static void sendLoginCharacterResult(Kaminari.Client<ProtocolQueues> client, StatusEx data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendLoginCharacterResult(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendLoginCharacterResult(Kaminari.Client<ProtocolQueues> client, StatusEx data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendLoginCharacterResult(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastLoginCharacterResult(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginCharacterResult(broadcaster, data, callback));
        }
        public static void broadcastLoginCharacterResult(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginCharacterResult(broadcaster, data));
        }
        public static void broadcastLoginCharacterResultSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginCharacterResultSingle(broadcaster, data, callback));
        }
        public static void broadcastLoginCharacterResultSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, StatusEx data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastLoginCharacterResultSingle(broadcaster, data));
        }
        public static void sendEnterWorld(Kaminari.Client<ProtocolQueues> client, Success data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendEnterWorld(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendEnterWorld(Kaminari.Client<ProtocolQueues> client, Success data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendEnterWorld(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastEnterWorld(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastEnterWorld(broadcaster, data, callback));
        }
        public static void broadcastEnterWorld(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastEnterWorld(broadcaster, data));
        }
        public static void broadcastEnterWorldSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastEnterWorldSingle(broadcaster, data, callback));
        }
        public static void broadcastEnterWorldSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Success data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastEnterWorldSingle(broadcaster, data));
        }
        public static void sendDoSth(Kaminari.Client<ProtocolQueues> client, Complex data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendDoSth(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendDoSth(Kaminari.Client<ProtocolQueues> client, Complex data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendDoSth(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastDoSth(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDoSth(broadcaster, data, callback));
        }
        public static void broadcastDoSth(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDoSth(broadcaster, data));
        }
        public static void broadcastDoSthSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDoSthSingle(broadcaster, data, callback));
        }
        public static void broadcastDoSthSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Complex data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDoSthSingle(broadcaster, data));
        }
        public static void sendSpawn(Kaminari.Client<ProtocolQueues> client, SpawnData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSpawn(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendSpawn(Kaminari.Client<ProtocolQueues> client, SpawnData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSpawn(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastSpawn(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawn(broadcaster, data, callback));
        }
        public static void broadcastSpawn(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawn(broadcaster, data));
        }
        public static void broadcastSpawnSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawnSingle(broadcaster, data, callback));
        }
        public static void broadcastSpawnSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SpawnData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawnSingle(broadcaster, data));
        }
        public static void sendSelectedCharacterSpawnData(Kaminari.Client<ProtocolQueues> client, CharacterSpawnData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSelectedCharacterSpawnData(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendSelectedCharacterSpawnData(Kaminari.Client<ProtocolQueues> client, CharacterSpawnData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSelectedCharacterSpawnData(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastSelectedCharacterSpawnData(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSelectedCharacterSpawnData(broadcaster, data, callback));
        }
        public static void broadcastSelectedCharacterSpawnData(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSelectedCharacterSpawnData(broadcaster, data));
        }
        public static void broadcastSelectedCharacterSpawnDataSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSelectedCharacterSpawnDataSingle(broadcaster, data, callback));
        }
        public static void broadcastSelectedCharacterSpawnDataSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, CharacterSpawnData data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSelectedCharacterSpawnDataSingle(broadcaster, data));
        }
        public static void sendSpawnedEntity(Kaminari.Client<ProtocolQueues> client, Spawn data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSpawnedEntity(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendSpawnedEntity(Kaminari.Client<ProtocolQueues> client, Spawn data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSpawnedEntity(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastSpawnedEntity(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawnedEntity(broadcaster, data, callback));
        }
        public static void broadcastSpawnedEntity(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawnedEntity(broadcaster, data));
        }
        public static void broadcastSpawnedEntitySingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawnedEntitySingle(broadcaster, data, callback));
        }
        public static void broadcastSpawnedEntitySingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Spawn data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSpawnedEntitySingle(broadcaster, data));
        }
        public static void sendDespawnedEntity(Kaminari.Client<ProtocolQueues> client, Despawn data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendDespawnedEntity(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendDespawnedEntity(Kaminari.Client<ProtocolQueues> client, Despawn data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendDespawnedEntity(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastDespawnedEntity(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDespawnedEntity(broadcaster, data, callback));
        }
        public static void broadcastDespawnedEntity(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDespawnedEntity(broadcaster, data));
        }
        public static void broadcastDespawnedEntitySingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDespawnedEntitySingle(broadcaster, data, callback));
        }
        public static void broadcastDespawnedEntitySingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, Despawn data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastDespawnedEntitySingle(broadcaster, data));
        }
        public static void sendWorldUpdate(Kaminari.Client<ProtocolQueues> client, EntityUpdate data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendWorldUpdate(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastWorldUpdate(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, EntityUpdate data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastWorldUpdate(broadcaster, data));
        }
        public static void broadcastWorldUpdateSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, EntityUpdate data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastWorldUpdateSingle(broadcaster, data));
        }
        public static void sendSelfWorldUpdate(Kaminari.Client<ProtocolQueues> client, SelfUpdate data, Action callback)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSelfWorldUpdate(client.getSuperPacket().getQueues(), data, callback));
        }
        public static void sendSelfWorldUpdate(Kaminari.Client<ProtocolQueues> client, SelfUpdate data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.sendSelfWorldUpdate(client.getSuperPacket().getQueues(), data));
        }
        public static void broadcastSelfWorldUpdate(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SelfUpdate data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSelfWorldUpdate(broadcaster, data));
        }
        public static void broadcastSelfWorldUpdateSingle(Kaminari.Client<ProtocolQueues> client, Kaminari.IBroadcaster<ProtocolQueues> broadcaster, SelfUpdate data)
        {
            client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcastSelfWorldUpdateSingle(broadcaster, data));
        }
    }

}
