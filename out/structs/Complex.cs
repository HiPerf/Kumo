package lostsouls.net.lostsocket.lostsouls.net.kumo.structs;
import java.util.ArrayList;
import java.util.TreeMap;
import net.kaminari.Packet;
import net.kaminari.PacketReader;
import net.kaminari.Optional;
import net.kaminari.IMarshal;
import net.kaminari.packers.IData;
import net.kaminari.packers.IHasId;
import net.kaminari.packers.IHasDataVector;
public class Complex implements IData
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.getData().write(this.x.hasValue());
        if (this.x.hasValue())
        {
            packet.getData().write((uint)this.x.getValue());
        }
        packet.getData().write((byte)this.y.size());
        for (SpawnData val : this.y)
        {
            val.pack(marshal, packet);
        }
        packet.getData().write((int)this.z);
        packet.getData().write(this.w.hasValue());
        if (this.w.hasValue())
        {
            packet.getData().write((byte)this.w.getValue().size());
            for (bool val : this.w.getValue())
            {
                packet.getData().write((bool)val);
            }
        }
    }
    public bool unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + Byte.BYTES > packet.bufferSize())
        {
            return false;
        }
        if (packet.getData().readByte() == 1)
        {
            if (packet.bytesRead() + marshal.size(uint.class) > packet.bufferSize())
            {
                return false;
            }
            this.x.setValue(packet.getData().readuint());
        }
        int size_y = Byte.toUnsignedInt(packet.getData().readByte());
        this.y = new List<SpawnData>();
        for (int i = 0; i < size_y; ++i)
        {
            SpawnData data = new SpawnData();
            if (data.unpack(marshal, packet))
            {
                this.y.add(data);
            }
            else
            {
                return false;
            }
        }
        if (packet.bytesRead() + marshal.size(int.class) > packet.bufferSize())
        {
            return false;
        }
        this.z = packet.getData().readint();
        if (packet.bytesRead() + Byte.BYTES > packet.bufferSize())
        {
            return false;
        }
        if (packet.getData().readByte() == 1)
        {
            int size_w = Byte.toUnsignedInt(packet.getData().readByte());
            if (packet.bytesRead() + size_w * marshal.size(bool.class) > packet.bufferSize())
            {
                return false;
            }
            this.w.setValue(new List<bool>());
            for (int i = 0; i < size_w; ++i)
            {
                this.w.getValue().add(packet.getData().readbool());
            }
        }
        return true;
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += Byte.BYTES;
        if (this.x.hasValue())
        {
            size += marshal.size(uint.class);
        }
        size += Byte.BYTES + this.y.size() * marshal.size(SpawnData.class);
        size += marshal.size(int.class);
        size += Byte.BYTES;
        if (this.w.hasValue())
        {
            size += Byte.BYTES + this.w.getValue().size() * marshal.size(bool.class);
        }
        return size;
    }
    public Optional<uint> x;
    public ArrayList<SpawnData> y;
    public int z;
    public Optional<ArrayList<bool>> w;
}

