namespace Kumo
{
    public interface IClient : Kaminari.IBaseClient
    {
        bool onMove(Position data, ulong timestamp);
        bool onHandshake(ClientHandshake data, ulong timestamp);
        bool onLoginCharacter(CharacterSelection data, ulong timestamp);
        bool onLogin(LoginData data, ulong timestamp);
        bool onCreateCharacter(CreationData data, ulong timestamp);
        bool onClientUpdate(ClientData data, ulong timestamp);
    }

}
