class Marshal extends IMarshal
{
    public int sizeofHasId()
    {
        int size = 0;
        size += marshal.sizeofInt64();
        return size;
    }
    public int sizeofSpawnData()
    {
        int size = 0;
        size += marshal.sizeofInt64();
        size += marshal.sizeofInt8();
        size += marshal.sizeofInt8();
        return size;
    }
    public int sizeofMovement()
    {
        int size = 0;
        size += marshal.sizeofInt8();
        return size;
    }
    public int sizeofInt8()
    {
        return Char.Bytes;
    }
    public int sizeofInt16()
    {
        return Short.Bytes;
    }
    public int sizeofInt32()
    {
        return Integer.Bytes;
    }
    public int sizeofInt64()
    {
        return Long.Bytes;
    }
    public int sizeofUint8()
    {
        return Byte.Bytes;
    }
    public int sizeofUint16()
    {
        return Short.Bytes;
    }
    public int sizeofUint32()
    {
        return Integer.Bytes;
    }
    public int sizeofUint64()
    {
        return Long.Bytes;
    }
    public int sizeofFloat()
    {
        return Float.Bytes;
    }
    public int sizeofDouble()
    {
        return Double.Bytes;
    }
    public int sizeofBool()
    {
        return Byte.Bytes;
    }
    public boolean handlePacket(Packet packet, IClient client)
    {
        switch (packet.opcode())
        {
            case Opcodes.opcodeDoSth:
                return handleDoSth(this, packet, client);
            case Opcodes.opcodeSpawn:
                return handleSpawn(this, packet, client);
            default:
                return false;
        }
    }
    private boolean handleDoSth(IMarshal marshal, PacketReader packet, IClient client)
    {
        Complex data = new Complex();
        if (!data.unpack(marshal, packet))
        {
            return false;
        }
        return client.onDoSth(client, data, packet.timestamp());
    }
    private boolean handleSpawn(IMarshal marshal, PacketReader packet, IClient client)
    {
        SpawnData data = new SpawnData();
        if (!data.unpack(marshal, packet))
        {
            return false;
        }
        return client.onSpawn(client, data, packet.timestamp());
    }
}

