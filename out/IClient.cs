public interface IClient : IBaseClient
{
    bool onLoginResponse(Status data, ulong timestamp);
    bool onHandshakeResponse(Status data, ulong timestamp);
    bool onDoSth(Complex data, ulong timestamp);
    bool onSpawn(SpawnData data, ulong timestamp);
}

