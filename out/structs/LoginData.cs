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
public class LoginData implements IData
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.getData().write((string)this.username);
        packet.getData().write((ulong)this.password0);
        packet.getData().write((ulong)this.password1);
        packet.getData().write((ulong)this.password2);
        packet.getData().write((ulong)this.password3);
    }
    public bool unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + marshal.size(Byte.class) > packet.bufferSize())
        {
            return false;
        }
        if (packet.bytesRead() + marshal.size(Byte.class) + packet.getData().peekByte() > packet.bufferSize())
        {
            return false;
        }
        this.username = packet.getData().readstring();
        if (packet.bytesRead() + marshal.size(ulong.class) > packet.bufferSize())
        {
            return false;
        }
        this.password0 = packet.getData().readulong();
        if (packet.bytesRead() + marshal.size(ulong.class) > packet.bufferSize())
        {
            return false;
        }
        this.password1 = packet.getData().readulong();
        if (packet.bytesRead() + marshal.size(ulong.class) > packet.bufferSize())
        {
            return false;
        }
        this.password2 = packet.getData().readulong();
        if (packet.bytesRead() + marshal.size(ulong.class) > packet.bufferSize())
        {
            return false;
        }
        this.password3 = packet.getData().readulong();
        return true;
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += marshal.size(Byte.class) + this.username.length();
        size += marshal.size(ulong.class);
        size += marshal.size(ulong.class);
        size += marshal.size(ulong.class);
        size += marshal.size(ulong.class);
        return size;
    }
    public string username;
    public ulong password0;
    public ulong password1;
    public ulong password2;
    public ulong password3;
}

