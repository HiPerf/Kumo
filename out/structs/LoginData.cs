using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class LoginData : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((string)this.username);
            packet.getData().write((ulong)this.password0);
            packet.getData().write((ulong)this.password1);
            packet.getData().write((ulong)this.password2);
            packet.getData().write((ulong)this.password3);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + marshal.size<byte>() > packet.bufferSize())
            {
                return false;
            }
            if (packet.bytesRead() + marshal.size<byte>() + packet.getData().peekByte() > packet.bufferSize())
            {
                return false;
            }
            this.username = packet.getData().readString();
            if (packet.bytesRead() + marshal.size<ulong>() > packet.bufferSize())
            {
                return false;
            }
            this.password0 = packet.getData().readUlong();
            if (packet.bytesRead() + marshal.size<ulong>() > packet.bufferSize())
            {
                return false;
            }
            this.password1 = packet.getData().readUlong();
            if (packet.bytesRead() + marshal.size<ulong>() > packet.bufferSize())
            {
                return false;
            }
            this.password2 = packet.getData().readUlong();
            if (packet.bytesRead() + marshal.size<ulong>() > packet.bufferSize())
            {
                return false;
            }
            this.password3 = packet.getData().readUlong();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<byte>() + this.username.Length;
            size += marshal.size<ulong>();
            size += marshal.size<ulong>();
            size += marshal.size<ulong>();
            size += marshal.size<ulong>();
            return size;
        }
        public string username;
        public ulong password0;
        public ulong password1;
        public ulong password2;
        public ulong password3;
    }

}
