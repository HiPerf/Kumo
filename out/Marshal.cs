public class Marshal : IMarshal, IHandlePacket
{
    public int size<T>()
    {
        if (typeof(T) == typeof(ClientHandshake))
        {
            int size = 0;
            size += this.size(uint.class);
            return size;
        }
        if (typeof(T) == typeof(Status))
        {
            int size = 0;
            size += this.size(bool.class);
            return size;
        }
        if (typeof(T) == typeof(HasId))
        {
            int size = 0;
            size += this.size(long.class);
            return size;
        }
        if (typeof(T) == typeof(SpawnData))
        {
            int size = 0;
            size += this.size(long.class);
            size += this.size(char.class);
            size += this.size(char.class);
            return size;
        }
        if (typeof(T) == typeof(Movement))
        {
            int size = 0;
            size += this.size(char.class);
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
    public bool handlePacket(PacketReader packet, IClient client)
    {
        switch (packet.getOpcode())
        {
            case Opcodes.opcodeLoginResponse:
                return handleLoginResponse(this, packet, client);
            case Opcodes.opcodeHandshakeResponse:
                return handleHandshakeResponse(this, packet, client);
            case Opcodes.opcodeDoSth:
                return handleDoSth(this, packet, client);
            case Opcodes.opcodeSpawn:
                return handleSpawn(this, packet, client);
            default:
                return false;
        }
    }
    private bool handleHandshakeResponse(IMarshal marshal, PacketReader packet, IClient client)
    {
        Status data = new Status();
        if (!data.unpack(marshal, packet))
        {
            return false;
        }
        return client.onHandshakeResponse(data, packet.timestamp());
    }
    private bool handleLoginResponse(IMarshal marshal, PacketReader packet, IClient client)
    {
        Status data = new Status();
        if (!data.unpack(marshal, packet))
        {
            return false;
        }
        return client.onLoginResponse(data, packet.timestamp());
    }
    private bool handleDoSth(IMarshal marshal, PacketReader packet, IClient client)
    {
        Complex data = new Complex();
        if (!data.unpack(marshal, packet))
        {
            return false;
        }
        return client.onDoSth(data, packet.timestamp());
    }
    private bool handleSpawn(IMarshal marshal, PacketReader packet, IClient client)
    {
        SpawnData data = new SpawnData();
        if (!data.unpack(marshal, packet))
        {
            return false;
        }
        return client.onSpawn(data, packet.timestamp());
    }
    public static Marshal instance;
}

