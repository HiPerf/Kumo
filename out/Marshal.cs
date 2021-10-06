namespace Kumo
{
    public class Marshal : Kaminari.IMarshal, Kaminari.IHandlePacket
    {
        public int size<T>()
        {
            if (typeof(T) == typeof(CharacterSelection))
            {
                int size = 0;
                size += this.size<byte>();
                return size;
            }
            if (typeof(T) == typeof(ClientData))
            {
                int size = 0;
                size += this.size<char>();
                size += this.size<char>();
                size += this.size<byte>();
                return size;
            }
            if (typeof(T) == typeof(ClientHandshake))
            {
                int size = 0;
                size += this.size<uint>();
                return size;
            }
            if (typeof(T) == typeof(Status))
            {
                int size = 0;
                size += this.size<bool>();
                return size;
            }
            if (typeof(T) == typeof(StatusEx))
            {
                int size = 0;
                size += this.size<byte>();
                return size;
            }
            if (typeof(T) == typeof(CharactersListData))
            {
                int size = 0;
                size += this.size<byte>();
                return size;
            }
            if (typeof(T) == typeof(Success))
            {
                int size = 0;
                return size;
            }
            if (typeof(T) == typeof(HasId))
            {
                int size = 0;
                size += this.size<ulong>();
                return size;
            }
            if (typeof(T) == typeof(SpawnData))
            {
                int size = 0;
                size += this.size<ulong>();
                size += this.size<char>();
                size += this.size<char>();
                return size;
            }
            if (typeof(T) == typeof(Position))
            {
                int size = 0;
                size += this.size<ulong>();
                size += this.size<float>();
                size += this.size<float>();
                return size;
            }
            if (typeof(T) == typeof(CharacterSpawnData))
            {
                int size = 0;
                size += this.size<ulong>();
                return size;
            }
            if (typeof(T) == typeof(Spawn))
            {
                int size = 0;
                size += this.size<ulong>();
                size += this.size<ushort>();
                size += this.size<float>();
                size += this.size<float>();
                return size;
            }
            if (typeof(T) == typeof(Despawn))
            {
                int size = 0;
                size += this.size<ulong>();
                return size;
            }
            if (typeof(T) == typeof(EntityUpdate))
            {
                int size = 0;
                size += this.size<ulong>();
                size += this.size<float>();
                size += this.size<float>();
                size += this.size<float>();
                size += this.size<float>();
                size += this.size<float>();
                return size;
            }
            if (typeof(T) == typeof(SelfUpdate))
            {
                int size = 0;
                size += this.size<float>();
                size += this.size<float>();
                size += this.size<float>();
                size += this.size<float>();
                size += this.size<float>();
                size += this.size<byte>();
                size += this.size<ushort>();
                return size;
            }
            if (typeof(T) == typeof(char))
            {
                return sizeof(char);
            }
            if (typeof(T) == typeof(short))
            {
                return sizeof(short);
            }
            if (typeof(T) == typeof(int))
            {
                return sizeof(int);
            }
            if (typeof(T) == typeof(long))
            {
                return sizeof(long);
            }
            if (typeof(T) == typeof(byte))
            {
                return sizeof(byte);
            }
            if (typeof(T) == typeof(ushort))
            {
                return sizeof(ushort);
            }
            if (typeof(T) == typeof(uint))
            {
                return sizeof(uint);
            }
            if (typeof(T) == typeof(ulong))
            {
                return sizeof(ulong);
            }
            if (typeof(T) == typeof(float))
            {
                return sizeof(float);
            }
            if (typeof(T) == typeof(double))
            {
                return sizeof(double);
            }
            if (typeof(T) == typeof(bool))
            {
                return sizeof(bool);
            }
            return 0;
        }
        public bool handlePacket<T>(Kaminari.PacketReader packet, T client, ushort blockId) where T : Kaminari.IBaseClient
        {
            switch (packet.getOpcode())
            {
                case (ushort)Opcodes.opcodeMove:
                    return handleMove(this, packet, (IClient)client, blockId);
                case (ushort)Opcodes.opcodeHandshake:
                    return handleHandshake(this, packet, (IClient)client, blockId);
                case (ushort)Opcodes.opcodeLoginCharacter:
                    return handleLoginCharacter(this, packet, (IClient)client, blockId);
                case (ushort)Opcodes.opcodeLogin:
                    return handleLogin(this, packet, (IClient)client, blockId);
                case (ushort)Opcodes.opcodeCreateCharacter:
                    return handleCreateCharacter(this, packet, (IClient)client, blockId);
                case (ushort)Opcodes.opcodeClientUpdate:
                    return handleClientUpdate(this, packet, (IClient)client, blockId);
                default:
                    return false;
            }
        }
        public  Marshal()
        {
            createCharacter = new SortedList<ushort, DataBuffer<Createcharacter>>();
            createCharacterBufferSize = 2;
            createCharacterLastPeeked = 0;
            createCharacterLastCalled = 0;
            clientUpdate = new SortedList<ushort, DataBuffer<Clientupdate>>();
            clientUpdateBufferSize = 2;
            clientUpdateLastPeeked = 0;
            clientUpdateLastCalled = 0;
            handshake = new SortedList<ushort, DataBuffer<Handshake>>();
            handshakeBufferSize = 2;
            handshakeLastPeeked = 0;
            handshakeLastCalled = 0;
            login = new SortedList<ushort, DataBuffer<Login>>();
            loginBufferSize = 2;
            loginLastPeeked = 0;
            loginLastCalled = 0;
            loginCharacter = new SortedList<ushort, DataBuffer<Logincharacter>>();
            loginCharacterBufferSize = 2;
            loginCharacterLastPeeked = 0;
            loginCharacterLastCalled = 0;
            move = new SortedList<ushort, DataBuffer<Move>>();
            moveBufferSize = 2;
            moveLastPeeked = 0;
            moveLastCalled = 0;
        }
        public void Update(IClient client, ushort blockId)
        {
            while (checkBuffer(createCharacter, blockId, createCharacterBufferSize))
            {
                client.oncreateCharacter(client, createCharacter[0].data, createCharacter.front().timestamp);
                createCharacterLastCalled = data.blockId;
                createCharacter.RemoveAt(0);
            }
            while (checkBuffer(clientUpdate, blockId, clientUpdateBufferSize))
            {
                client.onclientUpdate(client, clientUpdate[0].data, clientUpdate.front().timestamp);
                clientUpdateLastCalled = data.blockId;
                clientUpdate.RemoveAt(0);
            }
            while (checkBuffer(handshake, blockId, handshakeBufferSize))
            {
                client.onhandshake(client, handshake[0].data, handshake.front().timestamp);
                handshakeLastCalled = data.blockId;
                handshake.RemoveAt(0);
            }
            while (checkBuffer(login, blockId, loginBufferSize))
            {
                client.onlogin(client, login[0].data, login.front().timestamp);
                loginLastCalled = data.blockId;
                login.RemoveAt(0);
            }
            while (checkBuffer(loginCharacter, blockId, loginCharacterBufferSize))
            {
                client.onloginCharacter(client, loginCharacter[0].data, loginCharacter.front().timestamp);
                loginCharacterLastCalled = data.blockId;
                loginCharacter.RemoveAt(0);
            }
            while (checkBuffer(move, blockId, moveBufferSize))
            {
                client.onmove(client, move[0].data, move.front().timestamp);
                moveLastCalled = data.blockId;
                move.RemoveAt(0);
            }
        }
        protected T emplaceData<T>(SortedList<ushort, DataBuffer<T>> buffer, ushort blockId, ulong timestamp) where T : new
        {
            var data = new DataBuffer<T>
            {
                BlockId = blockId;
                Timestamp = timestamp;
                Data = new T();
            };
            buffer.Add(blockId, data);
            return data;
        }
        protected bool checkBuffer<T>(SortedList<ushort, DataBuffer<T>> buffer, ushort blockId, byte bufferSize) where T : new
        {
            return buffer.Count > 0 && Overflow.le(buffer[0].block_id, Overflow.sub(blockId, (ushort)bufferSize));
        }
        private bool handleCreateCharacter(Kaminari.IMarshal marshal, Kaminari.PacketReader packet, IClient client, ushort blockId)
        {
            if (!client.check(client, "status", ingame_status::in_world))
            {
                return client.handleClientError(client, packet.getOpcode());
            }
            if (Overflow.leq(blockId, createCharacterLastCalled))
            {
                // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
                return true;
            }
            var data = emplaceData(createCharacter, blockId, packet.timestamp());
            if (!data.unpack(marshal, packet))
            {
                return false;
            }
            // The user is assumed to provide all peek methods in C#
            // TODO: Test if the method exists in the class
            return client.peekCreateCharacter(data, packet.timestamp());
        }
        private bool handleClientUpdate(Kaminari.IMarshal marshal, Kaminari.PacketReader packet, IClient client, ushort blockId)
        {
            if (Overflow.leq(blockId, clientUpdateLastCalled))
            {
                // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
                return true;
            }
            var data = emplaceData(clientUpdate, blockId, packet.timestamp());
            if (!data.unpack(marshal, packet))
            {
                return false;
            }
            // The user is assumed to provide all peek methods in C#
            // TODO: Test if the method exists in the class
            return client.peekClientUpdate(data, packet.timestamp());
        }
        private bool handleHandshake(Kaminari.IMarshal marshal, Kaminari.PacketReader packet, IClient client, ushort blockId)
        {
            if (!client.check(client, "status", ingame_status::new_connection))
            {
                return client.handleClientError(client, packet.getOpcode());
            }
            if (Overflow.leq(blockId, handshakeLastCalled))
            {
                // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
                return true;
            }
            var data = emplaceData(handshake, blockId, packet.timestamp());
            if (!data.unpack(marshal, packet))
            {
                return false;
            }
            // The user is assumed to provide all peek methods in C#
            // TODO: Test if the method exists in the class
            return client.peekHandshake(data, packet.timestamp());
        }
        private bool handleLogin(Kaminari.IMarshal marshal, Kaminari.PacketReader packet, IClient client, ushort blockId)
        {
            if (!client.check(client, "status", ingame_status::handshake_done))
            {
                return client.handleClientError(client, packet.getOpcode());
            }
            if (Overflow.leq(blockId, loginLastCalled))
            {
                // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
                return true;
            }
            var data = emplaceData(login, blockId, packet.timestamp());
            if (!data.unpack(marshal, packet))
            {
                return false;
            }
            // The user is assumed to provide all peek methods in C#
            // TODO: Test if the method exists in the class
            return client.peekLogin(data, packet.timestamp());
        }
        private bool handleLoginCharacter(Kaminari.IMarshal marshal, Kaminari.PacketReader packet, IClient client, ushort blockId)
        {
            if (!client.check(client, "status", ingame_status::login_done))
            {
                return client.handleClientError(client, packet.getOpcode());
            }
            if (Overflow.leq(blockId, loginCharacterLastCalled))
            {
                // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
                return true;
            }
            var data = emplaceData(loginCharacter, blockId, packet.timestamp());
            if (!data.unpack(marshal, packet))
            {
                return false;
            }
            // The user is assumed to provide all peek methods in C#
            // TODO: Test if the method exists in the class
            return client.peekLoginCharacter(data, packet.timestamp());
        }
        private bool handleMove(Kaminari.IMarshal marshal, Kaminari.PacketReader packet, IClient client, ushort blockId)
        {
            if (!client.check(client, "status", ingame_status::in_world))
            {
                return client.handleClientError(client, packet.getOpcode());
            }
            if (Overflow.leq(blockId, moveLastCalled))
            {
                // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
                return true;
            }
            var data = emplaceData(move, blockId, packet.timestamp());
            if (!data.unpack(marshal, packet))
            {
                return false;
            }
            // The user is assumed to provide all peek methods in C#
            // TODO: Test if the method exists in the class
            return client.peekMove(data, packet.timestamp());
        }
        public static Marshal instance;
        private SortedList<DataBuffer<CreateCharacter>> createCharacter;
        private byte createCharacterBufferSize;
        private ushort createCharacterLastPeeked;
        private ushort createCharacterLastCalled;
        private SortedList<DataBuffer<ClientUpdate>> clientUpdate;
        private byte clientUpdateBufferSize;
        private ushort clientUpdateLastPeeked;
        private ushort clientUpdateLastCalled;
        private SortedList<DataBuffer<Handshake>> handshake;
        private byte handshakeBufferSize;
        private ushort handshakeLastPeeked;
        private ushort handshakeLastCalled;
        private SortedList<DataBuffer<Login>> login;
        private byte loginBufferSize;
        private ushort loginLastPeeked;
        private ushort loginLastCalled;
        private SortedList<DataBuffer<LoginCharacter>> loginCharacter;
        private byte loginCharacterBufferSize;
        private ushort loginCharacterLastPeeked;
        private ushort loginCharacterLastCalled;
        private SortedList<DataBuffer<Move>> move;
        private byte moveBufferSize;
        private ushort moveLastPeeked;
        private ushort moveLastCalled;
    }

    public class DataBuffer<T> where T : new
    {
        public T data;
        public ushort BlockId;
        public ulong Timestamp;
    }

}
