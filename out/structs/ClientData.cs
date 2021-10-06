using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class ClientData : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((char)this.x);
            packet.getData().write((char)this.y);
            packet.getData().write((byte)this.seq);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            this.x = packet.getData().readChar();
            this.y = packet.getData().readChar();
            this.seq = packet.getData().readByte();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<char>();
            size += marshal.size<char>();
            size += marshal.size<byte>();
            return size;
        }
        public char x;
        public char y;
        public byte seq;
    }

}
