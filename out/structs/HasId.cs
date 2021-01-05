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
public class HasId implements IData
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.getData().write((long)this.id);
    }
    public bool unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
        {
            return false;
        }
        this.id = packet.getData().readlong();
        return true;
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += marshal.size(long.class);
        return size;
    }
    public long id;
}

