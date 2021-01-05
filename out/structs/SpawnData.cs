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
public class SpawnData implements IHasId
{
    public Long getId()
    {
        return id;
    }
    public void setId(Long id)
    {
        this.id = id;
    }
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.getData().write((long)this.id);
        packet.getData().write((char)this.x);
        packet.getData().write((char)this.y);
    }
    public bool unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
        {
            return false;
        }
        this.id = packet.getData().readlong();
        this.x = packet.getData().readchar();
        this.y = packet.getData().readchar();
        return true;
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += marshal.size(long.class);
        size += marshal.size(char.class);
        size += marshal.size(char.class);
        return size;
    }
    public ulong id;
    public char x;
    public char y;
}

