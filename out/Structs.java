package net.lostsocket.lostsouls.engine.net.kumo;
import java.util.ArrayList;
import java.util.TreeMap;
import net.lostsocket.lostsouls.engine.net.IData;
import net.lostsocket.lostsouls.engine.net.IHasId;
import net.lostsocket.lostsouls.engine.net.IHasDataVector;
class Complex extends IData
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.writeBoolean(this.x.hasValue);
        if (this.x.hasValue)
        {
            packet.writeUint32(this.x.value);
        }
        packet.writeByte((byte)this.y.size());
        for (SpawnData val : this.y)
        {
            val.pack(marshal, packet);
        }
        packet.writeInt32(this.z);
        packet.writeBoolean(this.w.hasValue);
        if (this.w.hasValue)
        {
            packet.writeByte((byte)this.w.value.size());
            for (boolean val : this.w.value)
            {
                packet.writeBool(val);
            }
        }
    }
    public boolean unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + Byte.Bytes >= packet.bufferSize())
        {
            return false;
        }
        if (packet.readByte() == 1)
        {
            if (packet.bytesRead() + marshal.sizeofUint32() >= packet.bufferSize())
            {
                return false;
            }
            this.x.Value = packet.readUint32();
        }
        int size = Byte.toUnsignedInt(packet.readByte());
        this.y = new ArrayList<SpawnData>();
        for (int i = 0; i < size; ++i)
        {
            SpawnData data = new SpawnData();
            if (data.unpack(marshal, packet))
            {
                this.y.add(data);
            }
            else;
            {
                return false;
            }
        }
        if (packet.bytesRead() + marshal.sizeofInt32() >= packet.bufferSize())
        {
            return false;
        }
        this.z = packet.readInt32();
        if (packet.bytesRead() + Byte.Bytes >= packet.bufferSize())
        {
            return false;
        }
        if (packet.readByte() == 1)
        {
            int size = Byte.toUnsignedInt(packet.readByte());
            if (packet.bytesRead() + size * marshal.sizeofBool() >= packet.bufferSize())
            {
                return false;
            }
            this.w.Value = new ArrayList<boolean>();
            for (int i = 0; i < size; ++i)
            {
                this.w.Value.add(packet.readBool());
            }
        }
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += Byte.Bytes;
        if (this.x.hasValue)
        {
            size += marshal.sizeofUint32();
        }
        size += Byte.Bytes + this.y.size() * marshal.sizeofSpawnData();
        size += marshal.sizeofInt32();
        size += Byte.Bytes;
        if (this.w.hasValue)
        {
            size += Byte.Bytes + this.w.value.size() * marshal.sizeofBool();
        }
        return size;
    }
    public Optional<Integer> x;
    public ArrayList<SpawnData> y;
    public Integer z;
    public Optional<ArrayList<boolean>> w;
}

class HasId extends IData
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.writeInt64(this.id);
    }
    public boolean unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + marshal.sizeofInt64() >= packet.bufferSize())
        {
            return false;
        }
        this.id = packet.readInt64();
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += marshal.sizeofInt64();
        return size;
    }
    public Long id;
}

class SpawnData extends has_id
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.writeInt64(this.id);
        packet.writeInt8(this.x);
        packet.writeInt8(this.y);
    }
    public boolean unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + marshal.sizeofInt64() >= packet.bufferSize())
        {
            return false;
        }
        this.id = packet.readInt64();
        if (packet.bytesRead() + marshal.sizeofInt8() >= packet.bufferSize())
        {
            return false;
        }
        this.x = packet.readInt8();
        if (packet.bytesRead() + marshal.sizeofInt8() >= packet.bufferSize())
        {
            return false;
        }
        this.y = packet.readInt8();
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += marshal.sizeofInt64();
        size += marshal.sizeofInt8();
        size += marshal.sizeofInt8();
        return size;
    }
    public Char x;
    public Char y;
}

class Movement extends IData
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.writeInt8(this.direction);
    }
    public boolean unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + marshal.sizeofInt8() >= packet.bufferSize())
        {
            return false;
        }
        this.direction = packet.readInt8();
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += marshal.sizeofInt8();
        return size;
    }
    public Char direction;
}

