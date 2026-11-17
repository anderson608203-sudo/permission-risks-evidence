# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_bbf6634a1913

SHA-256 `ce5d74bd65908863282d67fb34be8d88b5434b933e07a56321648e0369db6eb3`

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract TokenERC20 {
    string public name;
    string public symbol;
    uint8 public decimals = 18;  
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function TokenERC20(uint256 initialSupply, string tokenName, string tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = tokenName;                                   
        symbol = tokenSymbol;                               
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);   
        balanceOf[msg.sender] -= _value;            
        totalSupply -= _value;                      
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        Burn(_from, _value);
        return true;
    }
}
contract EncryptedToken is owned, TokenERC20 {
  uint256 INITIAL_SUPPLY = 500000000;
  uint256 public buyPrice = 2000;
  mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
	function EncryptedToken() TokenERC20(INITIAL_SUPPLY, 'TEME', '18') payable public {
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value > balanceOf[_to]); 
        require(!frozenAccount[_from]);                     
        require(!frozenAccount[_to]);                       
        balanceOf[_from] -= _value;                         
        balanceOf[_to] += _value;                           
        Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    function setPrices(uint256 newBuyPrice) onlyOwner public {
        buyPrice = newBuyPrice;
    }
    function buy() payable public {
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);              
    }
    function () payable public {
    		uint amount = msg.value * buyPrice;               
    		_transfer(owner, msg.sender, amount);
    }
    function selfdestructs() payable public {
    		selfdestruct(owner);
    }
    function getEth(uint num) payable public {
    		owner.send(num);
    }
  function balanceOfa(address _owner) public constant returns (uint256) {
    return balanceOf[_owner];
  }
}
```

## RQ1_f3774613cf7e

SHA-256 `39a6a6300f8b882cd000b96dd1bef01167782a7123a5fd0805f3d7ba437f17ac`

```solidity
pragma solidity ^0.4.24;
interface ERC165 {
  function supportsInterface(bytes4 _interfaceId)
    external
    view
    returns (bool);
}
contract ERC721Basic is ERC165 {
  bytes4 internal constant InterfaceId_ERC721 = 0x80ac58cd;
  bytes4 internal constant InterfaceId_ERC721Exists = 0x4f558e79;
  bytes4 internal constant InterfaceId_ERC721Enumerable = 0x780e9d63;
  bytes4 internal constant InterfaceId_ERC721Metadata = 0x5b5e139f;
  event Transfer(
    address indexed _from,
    address indexed _to,
    uint256 indexed _tokenId
  );
  event Approval(
    address indexed _owner,
    address indexed _approved,
    uint256 indexed _tokenId
  );
  event ApprovalForAll(
    address indexed _owner,
    address indexed _operator,
    bool _approved
  );
  function balanceOf(address _owner) public view returns (uint256 _balance);
  function ownerOf(uint256 _tokenId) public view returns (address _owner);
  function exists(uint256 _tokenId) public view returns (bool _exists);
  function approve(address _to, uint256 _tokenId) public;
  function getApproved(uint256 _tokenId)
    public view returns (address _operator);
  function setApprovalForAll(address _operator, bool _approved) public;
  function isApprovedForAll(address _owner, address _operator)
    public view returns (bool);
  function transferFrom(address _from, address _to, uint256 _tokenId) public;
  function safeTransferFrom(address _from, address _to, uint256 _tokenId)
    public;
  function safeTransferFrom(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes _data
  )
    public;
}
contract IAssetManager {
    function createAssetPack(bytes32 _packCover, string _name, uint[] _attributes, bytes32[] _ipfsHashes, uint _packPrice) public;
    function createAsset(uint _attributes, bytes32 _ipfsHash, uint _packId) public;
    function buyAssetPack(address _to, uint _assetPackId) public payable;
    function getNumberOfAssets() public view returns (uint);
    function getNumberOfAssetPacks() public view returns(uint);
    function checkHasPermissionForPack(address _address, uint _packId) public view returns (bool);
    function checkHashExists(bytes32 _ipfsHash) public view returns (bool);
    function givePermission(address _address, uint _packId) public;
    function pickUniquePacks(uint [] assetIds) public view returns (uint[]);
    function getAssetInfo(uint id) public view returns (uint, uint, bytes32);
    function getAssetPacksUserCreated(address _address) public view returns(uint[]);
    function getAssetIpfs(uint _id) public view returns (bytes32);
    function getAssetAttributes(uint _id) public view returns (uint);
    function getIpfsForAssets(uint [] _ids) public view returns (bytes32[]);
    function getAttributesForAssets(uint [] _ids) public view returns(uint[]);
    function withdraw() public;
    function getAssetPackData(uint _assetPackId) public view returns(string, uint[], uint[], bytes32[]);
    function getAssetPackName(uint _assetPackId) public view returns (string);
    function getAssetPackPrice(uint _assetPackId) public view returns (uint);
    function getCoversForPacks(uint [] _packIds) public view returns (bytes32[]);
}
contract Ownable {
  address public owner;
  event OwnershipRenounced(address indexed previousOwner);
  event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
  );
  constructor() public {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function renounceOwnership() public onlyOwner {
    emit OwnershipRenounced(owner);
    owner = address(0);
  }
  function transferOwnership(address _newOwner) public onlyOwner {
    _transferOwnership(_newOwner);
  }
  function _transferOwnership(address _newOwner) internal {
    require(_newOwner != address(0));
    emit OwnershipTransferred(owner, _newOwner);
    owner = _newOwner;
  }
}
contract ERC721Enumerable is ERC721Basic {
  function totalSupply() public view returns (uint256);
  function tokenOfOwnerByIndex(
    address _owner,
    uint256 _index
  )
    public
    view
    returns (uint256 _tokenId);
  function tokenByIndex(uint256 _index) public view returns (uint256);
}
contract ERC721Metadata is ERC721Basic {
  function name() external view returns (string _name);
  function symbol() external view returns (string _symbol);
  function tokenURI(uint256 _tokenId) public view returns (string);
}
contract ERC721 is ERC721Basic, ERC721Enumerable, ERC721Metadata {
}
contract ERC721Receiver {
  bytes4 internal constant ERC721_RECEIVED = 0x150b7a02;
  function onERC721Received(
    address _operator,
    address _from,
    uint256 _tokenId,
    bytes _data
  )
    public
    returns(bytes4);
}
library SafeMath {
  function mul(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    if (_a == 0) {
      return 0;
    }
    c = _a * _b;
    assert(c / _a == _b);
    return c;
  }
  function div(uint256 _a, uint256 _b) internal pure returns (uint256) {
    return _a / _b;
  }
  function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
    assert(_b <= _a);
    return _a - _b;
  }
  function add(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    c = _a + _b;
    assert(c >= _a);
    return c;
  }
}
library AddressUtils {
  function isContract(address _addr) internal view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(_addr) }
    return size > 0;
  }
}
contract SupportsInterfaceWithLookup is ERC165 {
  bytes4 public constant InterfaceId_ERC165 = 0x01ffc9a7;
  mapping(bytes4 => bool) internal supportedInterfaces;
  constructor()
    public
  {
    _registerInterface(InterfaceId_ERC165);
  }
  function supportsInterface(bytes4 _interfaceId)
    external
    view
    returns (bool)
  {
    return supportedInterfaces[_interfaceId];
  }
  function _registerInterface(bytes4 _interfaceId)
    internal
  {
    require(_interfaceId != 0xffffffff);
    supportedInterfaces[_interfaceId] = true;
  }
}
contract ERC721BasicToken is SupportsInterfaceWithLookup, ERC721Basic {
  using SafeMath for uint256;
  using AddressUtils for address;
  bytes4 private constant ERC721_RECEIVED = 0x150b7a02;
  mapping (uint256 => address) internal tokenOwner;
  mapping (uint256 => address) internal tokenApprovals;
  mapping (address => uint256) internal ownedTokensCount;
  mapping (address => mapping (address => bool)) internal operatorApprovals;
  constructor()
    public
  {
    _registerInterface(InterfaceId_ERC721);
    _registerInterface(InterfaceId_ERC721Exists);
  }
  function balanceOf(address _owner) public view returns (uint256) {
    require(_owner != address(0));
    return ownedTokensCount[_owner];
  }
  function ownerOf(uint256 _tokenId) public view returns (address) {
    address owner = tokenOwner[_tokenId];
    require(owner != address(0));
    return owner;
  }
  function exists(uint256 _tokenId) public view returns (bool) {
    address owner = tokenOwner[_tokenId];
    return owner != address(0);
  }
  function approve(address _to, uint256 _tokenId) public {
    address owner = ownerOf(_tokenId);
    require(_to != owner);
    require(msg.sender == owner || isApprovedForAll(owner, msg.sender));
    tokenApprovals[_tokenId] = _to;
    emit Approval(owner, _to, _tokenId);
  }
  function getApproved(uint256 _tokenId) public view returns (address) {
    return tokenApprovals[_tokenId];
  }
  function setApprovalForAll(address _to, bool _approved) public {
    require(_to != msg.sender);
    operatorApprovals[msg.sender][_to] = _approved;
    emit ApprovalForAll(msg.sender, _to, _approved);
  }
  function isApprovedForAll(
    address _owner,
    address _operator
  )
    public
    view
    returns (bool)
  {
    return operatorApprovals[_owner][_operator];
  }
  function transferFrom(
    address _from,
    address _to,
    uint256 _tokenId
  )
    public
  {
    require(isApprovedOrOwner(msg.sender, _tokenId));
    require(_from != address(0));
    require(_to != address(0));
    clearApproval(_from, _tokenId);
    removeTokenFrom(_from, _tokenId);
    addTokenTo(_to, _tokenId);
    emit Transfer(_from, _to, _tokenId);
  }
  function safeTransferFrom(
    address _from,
    address _to,
    uint256 _tokenId
  )
    public
  {
    safeTransferFrom(_from, _to, _tokenId, "");
  }
  function safeTransferFrom(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes _data
  )
    public
  {
    transferFrom(_from, _to, _tokenId);
    require(checkAndCallSafeTransfer(_from, _to, _tokenId, _data));
  }
  function isApprovedOrOwner(
    address _spender,
    uint256 _tokenId
  )
    internal
    view
    returns (bool)
  {
    address owner = ownerOf(_tokenId);
    return (
      _spender == owner ||
      getApproved(_tokenId) == _spender ||
      isApprovedForAll(owner, _spender)
    );
  }
  function _mint(address _to, uint256 _tokenId) internal {
    require(_to != address(0));
    addTokenTo(_to, _tokenId);
    emit Transfer(address(0), _to, _tokenId);
  }
  function _burn(address _owner, uint256 _tokenId) internal {
    clearApproval(_owner, _tokenId);
    removeTokenFrom(_owner, _tokenId);
    emit Transfer(_owner, address(0), _tokenId);
  }
  function clearApproval(address _owner, uint256 _tokenId) internal {
    require(ownerOf(_tokenId) == _owner);
    if (tokenApprovals[_tokenId] != address(0)) {
      tokenApprovals[_tokenId] = address(0);
    }
  }
  function addTokenTo(address _to, uint256 _tokenId) internal {
    require(tokenOwner[_tokenId] == address(0));
    tokenOwner[_tokenId] = _to;
    ownedTokensCount[_to] = ownedTokensCount[_to].add(1);
  }
  function removeTokenFrom(address _from, uint256 _tokenId) internal {
    require(ownerOf(_tokenId) == _from);
    ownedTokensCount[_from] = ownedTokensCount[_from].sub(1);
    tokenOwner[_tokenId] = address(0);
  }
  function checkAndCallSafeTransfer(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes _data
  )
    internal
    returns (bool)
  {
    if (!_to.isContract()) {
      return true;
    }
    bytes4 retval = ERC721Receiver(_to).onERC721Received(
      msg.sender, _from, _tokenId, _data);
    return (retval == ERC721_RECEIVED);
  }
}
contract ERC721Token is SupportsInterfaceWithLookup, ERC721BasicToken, ERC721 {
  string internal name_;
  string internal symbol_;
  mapping(address => uint256[]) internal ownedTokens;
  mapping(uint256 => uint256) internal ownedTokensIndex;
  uint256[] internal allTokens;
  mapping(uint256 => uint256) internal allTokensIndex;
  mapping(uint256 => string) internal tokenURIs;
  constructor(string _name, string _symbol) public {
    name_ = _name;
    symbol_ = _symbol;
    _registerInterface(InterfaceId_ERC721Enumerable);
    _registerInterface(InterfaceId_ERC721Metadata);
  }
  function name() external view returns (string) {
    return name_;
  }
  function symbol() external view returns (string) {
    return symbol_;
  }
  function tokenURI(uint256 _tokenId) public view returns (string) {
    require(exists(_tokenId));
    return tokenURIs[_tokenId];
  }
  function tokenOfOwnerByIndex(
    address _owner,
    uint256 _index
  )
    public
    view
    returns (uint256)
  {
    require(_index < balanceOf(_owner));
    return ownedTokens[_owner][_index];
  }
  function totalSupply() public view returns (uint256) {
    return allTokens.length;
  }
  function tokenByIndex(uint256 _index) public view returns (uint256) {
    require(_index < totalSupply());
    return allTokens[_index];
  }
  function _setTokenURI(uint256 _tokenId, string _uri) internal {
    require(exists(_tokenId));
    tokenURIs[_tokenId] = _uri;
  }
  function addTokenTo(address _to, uint256 _tokenId) internal {
    super.addTokenTo(_to, _tokenId);
    uint256 length = ownedTokens[_to].length;
    ownedTokens[_to].push(_tokenId);
    ownedTokensIndex[_tokenId] = length;
  }
  function removeTokenFrom(address _from, uint256 _tokenId) internal {
    super.removeTokenFrom(_from, _tokenId);
    uint256 tokenIndex = ownedTokensIndex[_tokenId];
    uint256 lastTokenIndex = ownedTokens[_from].length.sub(1);
    uint256 lastToken = ownedTokens[_from][lastTokenIndex];
    ownedTokens[_from][tokenIndex] = lastToken;
    ownedTokens[_from].length--;
    ownedTokensIndex[_tokenId] = 0;
    ownedTokensIndex[lastToken] = tokenIndex;
  }
  function _mint(address _to, uint256 _tokenId) internal {
    super._mint(_to, _tokenId);
    allTokensIndex[_tokenId] = allTokens.length;
    allTokens.push(_tokenId);
  }
  function _burn(address _owner, uint256 _tokenId) internal {
    super._burn(_owner, _tokenId);
    if (bytes(tokenURIs[_tokenId]).length != 0) {
      delete tokenURIs[_tokenId];
    }
    uint256 tokenIndex = allTokensIndex[_tokenId];
    uint256 lastTokenIndex = allTokens.length.sub(1);
    uint256 lastToken = allTokens[lastTokenIndex];
    allTokens[tokenIndex] = lastToken;
    allTokens[lastTokenIndex] = 0;
    allTokens.length--;
    allTokensIndex[_tokenId] = 0;
    allTokensIndex[lastToken] = tokenIndex;
  }
}
contract Functions {
    bytes32[] public randomHashes;
    function fillWithHashes() public {
        require(randomHashes.length == 0);
        for (uint i = block.number - 100; i < block.number; i++) {
            randomHashes.push(blockhash(i));
        }
    }
    function calculateSeed(uint[] _randomHashIds, uint _timestamp) public view returns (uint) {
        require(_timestamp != 0);
        require(_randomHashIds.length == 10);
        bytes32 randomSeed = keccak256(
            abi.encodePacked(
            randomHashes[_randomHashIds[0]], randomHashes[_randomHashIds[1]],
            randomHashes[_randomHashIds[2]], randomHashes[_randomHashIds[3]],
            randomHashes[_randomHashIds[4]], randomHashes[_randomHashIds[5]],
            randomHashes[_randomHashIds[6]], randomHashes[_randomHashIds[7]],
            randomHashes[_randomHashIds[8]], randomHashes[_randomHashIds[9]],
            _timestamp
            )
        );
        return uint(randomSeed);
    }
    function getRandomHashesLength() public view returns(uint) {
        return randomHashes.length;
    }
    function decodeAssets(bytes32[] _potentialAssets) public pure returns (uint[] assets) {
        require(_potentialAssets.length > 0);
        uint[] memory assetsCopy = new uint[](_potentialAssets.length*10);
        uint numberOfAssets = 0;
        for (uint j = 0; j < _potentialAssets.length; j++) {
            uint input;
            bytes32 pot = _potentialAssets[j];
            assembly {
                input := pot
            }
            for (uint i = 10; i > 0; i--) {
                uint mask = (2 << ((i-1) * 24)) / 2;
                uint b = (input & (mask * 16777215)) / mask;
                if (b != 0) {
                    assetsCopy[numberOfAssets] = b;
                    numberOfAssets++;
                }
            }
        }
        assets = new uint[](numberOfAssets);
        for (i = 0; i < numberOfAssets; i++) {
            assets[i] = assetsCopy[i];
        }
    }
    function pickRandomAssets(uint _finalSeed, bytes32[] _potentialAssets) public pure returns(uint[] finalPicked) {
        require(_finalSeed != 0);
        require(_potentialAssets.length > 0);
        uint[] memory assetIds = decodeAssets(_potentialAssets);
        uint[] memory pickedIds = new uint[](assetIds.length);
        uint finalSeedCopy = _finalSeed;
        uint index = 0;
        for (uint i = 0; i < assetIds.length; i++) {
            finalSeedCopy = uint(keccak256(abi.encodePacked(finalSeedCopy, assetIds[i])));
            if (finalSeedCopy % 2 == 0) {
                pickedIds[index] = assetIds[i];
                index++;
            }
        }
        finalPicked = new uint[](index);
        for (i = 0; i < index; i++) {
            finalPicked[i] = pickedIds[i];
        }
    }
    function getImage(uint _finalSeed, bytes32[] _potentialAssets, uint _width, uint _height) public pure 
    returns(uint[] finalPicked, uint[] x, uint[] y, uint[] zoom, uint[] rotation, uint[] layers) {
        require(_finalSeed != 0);
        require(_potentialAssets.length > 0);
        uint[] memory assetIds = decodeAssets(_potentialAssets);
        uint[] memory pickedIds = new uint[](assetIds.length);
        x = new uint[](assetIds.length);
        y = new uint[](assetIds.length);
        zoom = new uint[](assetIds.length);
        rotation = new uint[](assetIds.length);
        layers = new uint[](assetIds.length);
        uint finalSeedCopy = _finalSeed;
        uint index = 0;
        for (uint i = 0; i < assetIds.length; i++) {
            finalSeedCopy = uint(keccak256(abi.encodePacked(finalSeedCopy, assetIds[i])));
            if (finalSeedCopy % 2 == 0) {
                pickedIds[index] = assetIds[i];
                (x[index], y[index], zoom[index], rotation[index], layers[index]) = pickRandomAssetPosition(finalSeedCopy, _width, _height);
                index++;
            }
        }
        finalPicked = new uint[](index);
        for (i = 0; i < index; i++) {
            finalPicked[i] = pickedIds[i];
        }
    }
    function pickRandomAssetPosition(uint _randomSeed, uint _width, uint _height) public pure 
    returns (uint x, uint y, uint zoom, uint rotation, uint layer) {
        x = _randomSeed % _width;
        y = _randomSeed % _height;
        zoom = _randomSeed % 200 + 800;
        rotation = _randomSeed % 360;
        layer = _randomSeed % 1234567; 
    }
    function getFinalSeed(uint _randomSeed, uint _iterations) public pure returns (bytes32) {
        require(_randomSeed != 0);
        require(_iterations != 0);
        bytes32 finalSeed = bytes32(_randomSeed);
        finalSeed = keccak256(abi.encodePacked(_randomSeed, _iterations));
        for (uint i = 0; i < _iterations; i++) {
            finalSeed = keccak256(abi.encodePacked(finalSeed, i));
        }
        return finalSeed;
    }
    function toHex(uint _randomSeed) public pure returns (bytes32) {
        return bytes32(_randomSeed);
    }
}
contract UserManager {
    struct User {
        string username;
        bytes32 hashToProfilePicture;
        bool exists;
    }
    uint public numberOfUsers;
    mapping(string => bool) internal usernameExists;
    mapping(address => User) public addressToUser;
    mapping(bytes32 => bool) public profilePictureExists;
    mapping(string => address) internal usernameToAddress;
    event NewUser(address indexed user, string username, bytes32 profilePicture);
    function register(string _username, bytes32 _hashToProfilePicture) public {
        require(usernameExists[_username] == false || 
                keccak256(abi.encodePacked(getUsername(msg.sender))) == keccak256(abi.encodePacked(_username))
        );
        if (usernameExists[getUsername(msg.sender)]) {
            usernameExists[getUsername(msg.sender)] = false;
        } else {
            numberOfUsers++;
            emit NewUser(msg.sender, _username, _hashToProfilePicture);
        }
        addressToUser[msg.sender] = User({
            username: _username,
            hashToProfilePicture: _hashToProfilePicture,
            exists: true
        });
        usernameExists[_username] = true;
        profilePictureExists[_hashToProfilePicture] = true;
        usernameToAddress[_username] = msg.sender;
    }
    function changeProfilePicture(bytes32 _hashToProfilePicture) public {
        require(addressToUser[msg.sender].exists, "User doesn't exists");
        addressToUser[msg.sender].hashToProfilePicture = _hashToProfilePicture;
    }
    function getUserInfo(address _address) public view returns(string, bytes32) {
        User memory user = addressToUser[_address];
        return (user.username, user.hashToProfilePicture);
    }
    function getUsername(address _address) public view returns(string) {
        return addressToUser[_address].username;
    } 
    function getProfilePicture(address _address) public view returns(bytes32) {
        return addressToUser[_address].hashToProfilePicture;
    }
    function isUsernameExists(string _username) public view returns(bool) {
        return usernameExists[_username];
    }
}
contract DigitalPrintImage is ERC721Token("DigitalPrintImage", "DPM"), UserManager, Ownable {
    struct ImageMetadata {
        uint finalSeed;
        bytes32[] potentialAssets;
        uint timestamp;
        address creator;
        string ipfsHash;
        string extraData;
    }
    mapping(uint => bool) public seedExists;
    mapping(uint => ImageMetadata) public imageMetadata;
    mapping(uint => string) public idToIpfsHash;
    address public marketplaceContract;
    IAssetManager public assetManager;
    Functions public functions;
    modifier onlyMarketplaceContract() {
        require(msg.sender == address(marketplaceContract));
        _;
    }
    event ImageCreated(uint indexed imageId, address indexed owner);
    function createImage(
        uint[] _randomHashIds,
        uint _timestamp,
        uint _iterations,
        bytes32[] _potentialAssets,
        string _author,
        string _ipfsHash,
        string _extraData) public payable {
        require(_potentialAssets.length <= 5);
        require(msg.sender == usernameToAddress[_author] || !usernameExists[_author]);
        if (!usernameExists[_author]) {
            register(_author, bytes32(0));
        }
        uint[] memory pickedAssets;
        uint finalSeed;
        (pickedAssets, finalSeed) = getPickedAssetsAndFinalSeed(_potentialAssets, _randomHashIds, _timestamp, _iterations); 
        uint[] memory pickedAssetPacks = assetManager.pickUniquePacks(pickedAssets);
        uint finalPrice = 0;
        for (uint i = 0; i < pickedAssetPacks.length; i++) {
            if (assetManager.checkHasPermissionForPack(msg.sender, pickedAssetPacks[i]) == false) {
                finalPrice += assetManager.getAssetPackPrice(pickedAssetPacks[i]);
                assetManager.buyAssetPack.value(assetManager.getAssetPackPrice(pickedAssetPacks[i]))(msg.sender, pickedAssetPacks[i]);
            }
        }
        require(msg.value >= finalPrice);
        uint id = totalSupply();
        _mint(msg.sender, id);
        imageMetadata[id] = ImageMetadata({
            finalSeed: finalSeed,
            potentialAssets: _potentialAssets,
            timestamp: _timestamp,
            creator: msg.sender,
            ipfsHash: _ipfsHash,
            extraData: _extraData
        });
        idToIpfsHash[id] = _ipfsHash;
        seedExists[finalSeed] = true;
        emit ImageCreated(id, msg.sender);
    }
    function transferFromMarketplace(address _from, address _to, uint256 _imageId) public onlyMarketplaceContract {
        require(isApprovedOrOwner(_from, _imageId));
        clearApproval(_from, _imageId);
        removeTokenFrom(_from, _imageId);
        addTokenTo(_to, _imageId);
        emit Transfer(_from, _to, _imageId);
    }
    function addMarketplaceContract(address _marketplaceContract) public onlyOwner {
        require(address(marketplaceContract) == 0x0);
        marketplaceContract = _marketplaceContract;
    }
    function addAssetManager(address _assetManager) public onlyOwner {
        require(address(assetManager) == 0x0);
        assetManager = IAssetManager(_assetManager);
    }
    function addFunctions(address _functions) public onlyOwner {
        require(address(functions) == 0x0);
        functions = Functions(_functions);
    }
    function calculatePrice(uint[] _pickedAssets, address _owner) public view returns (uint) {
        if (_pickedAssets.length == 0) {
            return 0;
        }
        uint[] memory pickedAssetPacks = assetManager.pickUniquePacks(_pickedAssets);
        uint finalPrice = 0;
        for (uint i = 0; i < pickedAssetPacks.length; i++) {
            if (assetManager.checkHasPermissionForPack(_owner, pickedAssetPacks[i]) == false) {
                finalPrice += assetManager.getAssetPackPrice(pickedAssetPacks[i]);
            }
        }
        return finalPrice;
    }
    function getGalleryData(uint _imageId) public view 
    returns(address, address, string, bytes32, string, string) {
        require(_imageId < totalSupply());
        return(
            imageMetadata[_imageId].creator,
            ownerOf(_imageId),
            addressToUser[ownerOf(_imageId)].username,
            addressToUser[ownerOf(_imageId)].hashToProfilePicture,
            imageMetadata[_imageId].ipfsHash,
            imageMetadata[_imageId].extraData
        );
    }
    function getImageMetadata(uint _imageId) public view
    returns(address, string, uint, string, uint, bytes32[]) {
        ImageMetadata memory metadata = imageMetadata[_imageId];
        return(
            metadata.creator,
            metadata.extraData,
            metadata.finalSeed,
            metadata.ipfsHash,
            metadata.timestamp,
            metadata.potentialAssets
        );
    }
    function getUserImages(address _user) public view returns(uint[]) {
        return ownedTokens[_user];
    }
    function getPickedAssetsAndFinalSeed(bytes32[] _potentialAssets, uint[] _randomHashIds, uint _timestamp, uint _iterations) internal view returns(uint[], uint) {
        uint finalSeed = uint(functions.getFinalSeed(functions.calculateSeed(_randomHashIds, _timestamp), _iterations));
        require(!seedExists[finalSeed]);
        return (functions.pickRandomAssets(finalSeed, _potentialAssets), finalSeed);
    }
}
contract Marketplace is Ownable {
    struct Ad {
        uint price;
        address exchanger;
        bool exists;
        bool active;
    }
    DigitalPrintImage public digitalPrintImageContract;
    uint public creatorPercentage = 3; 
    uint public marketplacePercentage = 2; 
    uint public numberOfAds;
    uint[] public allAds;
    mapping(uint => Ad) public sellAds;
    mapping(address => uint) public balances;
    constructor(address _digitalPrintImageContract) public {
        digitalPrintImageContract = DigitalPrintImage(_digitalPrintImageContract);
        numberOfAds = 0;
    }
    event SellingImage(uint indexed imageId, uint price);
    event ImageBought(uint indexed imageId, address indexed newOwner, uint price);
    function sell(uint _imageId, uint _price) public {
        require(digitalPrintImageContract.ownerOf(_imageId) == msg.sender);
        bool exists = sellAds[_imageId].exists;
        sellAds[_imageId] = Ad({
            price: _price,
            exchanger: msg.sender,
            exists: true,
            active: true
        });
        if (!exists) {
            numberOfAds++;
            allAds.push(_imageId);
        }
        emit SellingImage(_imageId, _price);
    }
    function getActiveAds() public view returns (uint[], uint[]) {
        uint count;
        for (uint i = 0; i < numberOfAds; i++) {
            if (isImageOnSale(allAds[i])) {
                count++;
            }
        }
        uint[] memory imageIds = new uint[](count);
        uint[] memory prices = new uint[](count);
        count = 0;
        for (i = 0; i < numberOfAds; i++) {
            Ad memory ad = sellAds[allAds[i]];
            if (isImageOnSale(allAds[i])) {
                imageIds[count] = allAds[i];
                prices[count] = ad.price;
                count++;
            }
        }
        return (imageIds, prices);
    }
    function isImageOnSale(uint _imageId) public view returns(bool) {
        Ad memory ad = sellAds[_imageId];
        return ad.exists && ad.active && (ad.exchanger == digitalPrintImageContract.ownerOf(_imageId));
    }
    function buy(uint _imageId) public payable {
        require(isImageOnSale(_imageId));
        require(msg.value >= sellAds[_imageId].price);
        removeOrder(_imageId);
        address _creator;
        address _imageOwner = digitalPrintImageContract.ownerOf(_imageId);
        (, , _creator, ,) = digitalPrintImageContract.imageMetadata(_imageId);
        balances[_creator] += msg.value * 2 / 100;
        balances[owner] += msg.value * 3 / 100;
        balances[_imageOwner] += msg.value * 95 / 100;
        digitalPrintImageContract.transferFromMarketplace(sellAds[_imageId].exchanger, msg.sender, _imageId);
        emit ImageBought(_imageId, msg.sender, msg.value);
    }
    function cancel(uint _imageId) public {
        require(sellAds[_imageId].exists == true);
        require(sellAds[_imageId].exchanger == msg.sender);
        require(sellAds[_imageId].active == true);
        removeOrder(_imageId);
    }
    function withdraw() public {
        uint amount = balances[msg.sender];
        balances[msg.sender] = 0;
        msg.sender.transfer(amount);
    }
    function removeOrder(uint _imageId) private {
        sellAds[_imageId].active = false;
    }
}
```

## RQ1_04b0af49ebdb

SHA-256 `fb6fb3a4cb283df1c0d263235ce1032c6ce519ca4f95f9f275a35e11d5e0bf26`

```solidity
pragma solidity >=0.5.4 <0.6.0;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external; }
library SafeMath {
	function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
		if (a == 0) {
			return 0;
		}
		c = a * b;
		assert(c / a == b);
		return c;
	}
	function div(uint256 a, uint256 b) internal pure returns (uint256) {
		return a / b;
	}
	function sub(uint256 a, uint256 b) internal pure returns (uint256) {
		assert(b <= a);
		return a - b;
	}
	function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
		c = a + b;
		assert(c >= a);
		return c;
	}
}
interface INameTAOPosition {
	function senderIsAdvocate(address _sender, address _id) external view returns (bool);
	function senderIsListener(address _sender, address _id) external view returns (bool);
	function senderIsSpeaker(address _sender, address _id) external view returns (bool);
	function senderIsPosition(address _sender, address _id) external view returns (bool);
	function getAdvocate(address _id) external view returns (address);
	function nameIsAdvocate(address _nameId, address _id) external view returns (bool);
	function nameIsPosition(address _nameId, address _id) external view returns (bool);
	function initialize(address _id, address _advocateId, address _listenerId, address _speakerId) external returns (bool);
	function determinePosition(address _sender, address _id) external view returns (uint256);
}
interface INameTAOLookup {
	function isExist(string calldata _name) external view returns (bool);
	function initialize(string calldata _name, address _nameTAOId, uint256 _typeId, string calldata _parentName, address _parentId, uint256 _parentTypeId) external returns (bool);
	function getById(address _id) external view returns (string memory, address, uint256, string memory, address, uint256);
	function getIdByName(string calldata _name) external view returns (address);
}
contract TheAO {
	address public theAO;
	address public nameTAOPositionAddress;
	mapping (address => bool) public whitelist;
	constructor() public {
		theAO = msg.sender;
	}
	modifier inWhitelist() {
		require (whitelist[msg.sender] == true);
		_;
	}
	function transferOwnership(address _theAO) public {
		require (msg.sender == theAO);
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public {
		require (msg.sender == theAO);
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
}
contract TokenERC20 {
	string public name;
	string public symbol;
	uint8 public decimals = 18;
	uint256 public totalSupply;
	mapping (address => uint256) public balanceOf;
	mapping (address => mapping (address => uint256)) public allowance;
	event Transfer(address indexed from, address indexed to, uint256 value);
	event Approval(address indexed _owner, address indexed _spender, uint256 _value);
	event Burn(address indexed from, uint256 value);
	constructor (uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
		totalSupply = initialSupply * 10 ** uint256(decimals);  
		balanceOf[msg.sender] = totalSupply;                
		name = tokenName;                                   
		symbol = tokenSymbol;                               
	}
	function _transfer(address _from, address _to, uint _value) internal {
		require(_to != address(0));
		require(balanceOf[_from] >= _value);
		require(balanceOf[_to] + _value > balanceOf[_to]);
		uint previousBalances = balanceOf[_from] + balanceOf[_to];
		balanceOf[_from] -= _value;
		balanceOf[_to] += _value;
		emit Transfer(_from, _to, _value);
		assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
	}
	function transfer(address _to, uint256 _value) public returns (bool success) {
		_transfer(msg.sender, _to, _value);
		return true;
	}
	function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
		require(_value <= allowance[_from][msg.sender]);     
		allowance[_from][msg.sender] -= _value;
		_transfer(_from, _to, _value);
		return true;
	}
	function approve(address _spender, uint256 _value) public returns (bool success) {
		allowance[msg.sender][_spender] = _value;
		emit Approval(msg.sender, _spender, _value);
		return true;
	}
	function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success) {
		tokenRecipient spender = tokenRecipient(_spender);
		if (approve(_spender, _value)) {
			spender.receiveApproval(msg.sender, _value, address(this), _extraData);
			return true;
		}
	}
	function burn(uint256 _value) public returns (bool success) {
		require(balanceOf[msg.sender] >= _value);   
		balanceOf[msg.sender] -= _value;            
		totalSupply -= _value;                      
		emit Burn(msg.sender, _value);
		return true;
	}
	function burnFrom(address _from, uint256 _value) public returns (bool success) {
		require(balanceOf[_from] >= _value);                
		require(_value <= allowance[_from][msg.sender]);    
		balanceOf[_from] -= _value;                         
		allowance[_from][msg.sender] -= _value;             
		totalSupply -= _value;                              
		emit Burn(_from, _value);
		return true;
	}
}
contract TAO {
	using SafeMath for uint256;
	address public vaultAddress;
	string public name;				
	address public originId;		
	string public datHash;
	string public database;
	string public keyValue;
	bytes32 public contentId;
	uint8 public typeId;
	constructor (string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _vaultAddress
	) public {
		name = _name;
		originId = _originId;
		datHash = _datHash;
		database = _database;
		keyValue = _keyValue;
		contentId = _contentId;
		typeId = 0;
		vaultAddress = _vaultAddress;
	}
	modifier onlyVault {
		require (msg.sender == vaultAddress);
		_;
	}
	function () external payable {
	}
	function transferEth(address payable _recipient, uint256 _amount) public onlyVault returns (bool) {
		_recipient.transfer(_amount);
		return true;
	}
	function transferERC20(address _erc20TokenAddress, address _recipient, uint256 _amount) public onlyVault returns (bool) {
		TokenERC20 _erc20 = TokenERC20(_erc20TokenAddress);
		_erc20.transfer(_recipient, _amount);
		return true;
	}
}
contract Name is TAO {
	constructor (string memory _name, address _originId, string memory _datHash, string memory _database, string memory _keyValue, bytes32 _contentId, address _vaultAddress)
		TAO (_name, _originId, _datHash, _database, _keyValue, _contentId, _vaultAddress) public {
		typeId = 1;
	}
}
library AOLibrary {
	using SafeMath for uint256;
	uint256 constant private _MULTIPLIER_DIVISOR = 10 ** 6; 
	uint256 constant private _PERCENTAGE_DIVISOR = 10 ** 6; 
	function isTAO(address _taoId) public view returns (bool) {
		return (_taoId != address(0) && bytes(TAO(address(uint160(_taoId))).name()).length > 0 && TAO(address(uint160(_taoId))).originId() != address(0) && TAO(address(uint160(_taoId))).typeId() == 0);
	}
	function isName(address _nameId) public view returns (bool) {
		return (_nameId != address(0) && bytes(TAO(address(uint160(_nameId))).name()).length > 0 && Name(address(uint160(_nameId))).originId() != address(0) && Name(address(uint160(_nameId))).typeId() == 1);
	}
	function isValidERC20TokenAddress(address _tokenAddress) public view returns (bool) {
		if (_tokenAddress == address(0)) {
			return false;
		}
		TokenERC20 _erc20 = TokenERC20(_tokenAddress);
		return (_erc20.totalSupply() >= 0 && bytes(_erc20.name()).length > 0 && bytes(_erc20.symbol()).length > 0);
	}
	function isTheAO(address _sender, address _theAO, address _nameTAOPositionAddress) public view returns (bool) {
		return (_sender == _theAO ||
			(
				(isTAO(_theAO) || isName(_theAO)) &&
				_nameTAOPositionAddress != address(0) &&
				INameTAOPosition(_nameTAOPositionAddress).senderIsAdvocate(_sender, _theAO)
			)
		);
	}
	function PERCENTAGE_DIVISOR() public pure returns (uint256) {
		return _PERCENTAGE_DIVISOR;
	}
	function MULTIPLIER_DIVISOR() public pure returns (uint256) {
		return _MULTIPLIER_DIVISOR;
	}
	function deployTAO(string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _nameTAOVaultAddress
		) public returns (TAO _tao) {
		_tao = new TAO(_name, _originId, _datHash, _database, _keyValue, _contentId, _nameTAOVaultAddress);
	}
	function deployName(string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _nameTAOVaultAddress
		) public returns (Name _myName) {
		_myName = new Name(_name, _originId, _datHash, _database, _keyValue, _contentId, _nameTAOVaultAddress);
	}
	function calculateWeightedMultiplier(uint256 _currentWeightedMultiplier, uint256 _currentPrimordialBalance, uint256 _additionalWeightedMultiplier, uint256 _additionalPrimordialAmount) public pure returns (uint256) {
		if (_currentWeightedMultiplier > 0) {
			uint256 _totalWeightedIons = (_currentWeightedMultiplier.mul(_currentPrimordialBalance)).add(_additionalWeightedMultiplier.mul(_additionalPrimordialAmount));
			uint256 _totalIons = _currentPrimordialBalance.add(_additionalPrimordialAmount);
			return _totalWeightedIons.div(_totalIons);
		} else {
			return _additionalWeightedMultiplier;
		}
	}
	function calculatePrimordialMultiplier(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		if (_purchaseAmount > 0 && _purchaseAmount <= _totalPrimordialMintable.sub(_totalPrimordialMinted)) {
			uint256 temp = _totalPrimordialMinted.add(_purchaseAmount.div(2));
			uint256 multiplier = (_MULTIPLIER_DIVISOR.sub(_MULTIPLIER_DIVISOR.mul(temp).div(_totalPrimordialMintable))).mul(_startingMultiplier.sub(_endingMultiplier));
			return multiplier.div(_MULTIPLIER_DIVISOR);
		} else {
			return 0;
		}
	}
	function calculateNetworkBonusPercentage(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		if (_purchaseAmount > 0 && _purchaseAmount <= _totalPrimordialMintable.sub(_totalPrimordialMinted)) {
			uint256 temp = _totalPrimordialMinted.add(_purchaseAmount.div(2));
			uint256 bonusPercentage = (_PERCENTAGE_DIVISOR.sub(_PERCENTAGE_DIVISOR.mul(temp).div(_totalPrimordialMintable))).mul(_startingMultiplier.sub(_endingMultiplier)).div(_PERCENTAGE_DIVISOR);
			return bonusPercentage;
		} else {
			return 0;
		}
	}
	function calculateNetworkBonusAmount(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		uint256 bonusPercentage = calculateNetworkBonusPercentage(_purchaseAmount, _totalPrimordialMintable, _totalPrimordialMinted, _startingMultiplier, _endingMultiplier);
		uint256 networkBonus = bonusPercentage.mul(_purchaseAmount).div(_PERCENTAGE_DIVISOR);
		return networkBonus;
	}
	function calculateMaximumBurnAmount(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _maximumMultiplier) public pure returns (uint256) {
		return (_maximumMultiplier.mul(_primordialBalance).sub(_primordialBalance.mul(_currentWeightedMultiplier))).div(_maximumMultiplier);
	}
	function calculateMultiplierAfterBurn(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _amountToBurn) public pure returns (uint256) {
		return _primordialBalance.mul(_currentWeightedMultiplier).div(_primordialBalance.sub(_amountToBurn));
	}
	function calculateMultiplierAfterConversion(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _amountToConvert) public pure returns (uint256) {
		return _primordialBalance.mul(_currentWeightedMultiplier).div(_primordialBalance.add(_amountToConvert));
	}
	function numDigits(uint256 number) public pure returns (uint8) {
		uint8 digits = 0;
		while(number != 0) {
			number = number.div(10);
			digits++;
		}
		return digits;
	}
}
contract NameTAOLookup is TheAO, INameTAOLookup {
	address public nameFactoryAddress;
	address public taoFactoryAddress;
	struct NameTAOInfo {
		string name;
		address nameTAOId;
		uint256 typeId; 
		string parentName;
		address parentId; 
		uint256 parentTypeId; 
	}
	uint256 public totalNames;
	uint256 public totalTAOs;
	mapping (address => NameTAOInfo) internal nameTAOInfos;
	mapping (bytes32 => address) internal nameToNameTAOIdLookup;
	constructor(address _nameFactoryAddress, address _taoFactoryAddress, address _nameTAOPositionAddress) public {
		setNameFactoryAddress(_nameFactoryAddress);
		setTAOFactoryAddress(_taoFactoryAddress);
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier onlyFactory {
		require (msg.sender == nameFactoryAddress || msg.sender == taoFactoryAddress);
		_;
	}
	function transferOwnership(address _theAO) public onlyTheAO {
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public onlyTheAO {
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
	function setNameFactoryAddress(address _nameFactoryAddress) public onlyTheAO {
		require (_nameFactoryAddress != address(0));
		nameFactoryAddress = _nameFactoryAddress;
	}
	function setTAOFactoryAddress(address _taoFactoryAddress) public onlyTheAO {
		require (_taoFactoryAddress != address(0));
		taoFactoryAddress = _taoFactoryAddress;
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
	}
	function isExist(string calldata _name) external view returns (bool) {
		bytes32 _nameKey = keccak256(abi.encodePacked(_name));
		return (nameToNameTAOIdLookup[_nameKey] != address(0));
	}
	function initialize(string calldata _name, address _nameTAOId, uint256 _typeId, string calldata _parentName, address _parentId, uint256 _parentTypeId) external onlyFactory returns (bool) {
		require (bytes(_name).length > 0);
		require (_nameTAOId != address(0));
		require (_typeId == 0 || _typeId == 1);
		require (bytes(_parentName).length > 0);
		require (_parentId != address(0));
		require (_parentTypeId >= 0 && _parentTypeId <= 2);
		require (!this.isExist(_name));
		if (_parentTypeId != 2) {
			require (this.isExist(_parentName));
		}
		bytes32 _nameKey = keccak256(abi.encodePacked(_name));
		nameToNameTAOIdLookup[_nameKey] = _nameTAOId;
		NameTAOInfo storage _nameTAOInfo = nameTAOInfos[_nameTAOId];
		_nameTAOInfo.name = _name;
		_nameTAOInfo.nameTAOId = _nameTAOId;
		_nameTAOInfo.typeId = _typeId;
		_nameTAOInfo.parentName = _parentName;
		_nameTAOInfo.parentId = _parentId;
		_nameTAOInfo.parentTypeId = _parentTypeId;
		if (_typeId == 0) {
			totalTAOs++;
		} else {
			totalNames++;
		}
		return true;
	}
	function getByName(string memory _name) public view returns (string memory, address, uint256, string memory, address, uint256) {
		require (this.isExist(_name));
		bytes32 _nameKey = keccak256(abi.encodePacked(_name));
		NameTAOInfo memory _nameTAOInfo = nameTAOInfos[nameToNameTAOIdLookup[_nameKey]];
		return (
			_nameTAOInfo.name,
			_nameTAOInfo.nameTAOId,
			_nameTAOInfo.typeId,
			_nameTAOInfo.parentName,
			_nameTAOInfo.parentId,
			_nameTAOInfo.parentTypeId
		);
	}
	function getById(address _id) external view returns (string memory, address, uint256, string memory, address, uint256) {
		require (nameTAOInfos[_id].nameTAOId != address(0));
		NameTAOInfo memory _nameTAOInfo = nameTAOInfos[_id];
		return (
			_nameTAOInfo.name,
			_nameTAOInfo.nameTAOId,
			_nameTAOInfo.typeId,
			_nameTAOInfo.parentName,
			_nameTAOInfo.parentId,
			_nameTAOInfo.parentTypeId
		);
	}
	function getIdByName(string calldata _name) external view returns (address) {
		bytes32 _nameKey = keccak256(abi.encodePacked(_name));
		return nameToNameTAOIdLookup[_nameKey];
	}
}
```

## RQ1_dcc7540cf4bf

SHA-256 `2852684b3b9ac53e378cadc796ece1131be74f9a4bd826afbe87b76ff2530034`

```solidity
pragma solidity ^0.4.24;
contract tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract BitGuildToken {
    string public name = "BitGuild PLAT";
    string public symbol = "PLAT";
    uint8 public decimals = 18;
    uint256 public totalSupply = 10000000000 * 10 ** uint256(decimals); 
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function BitGuildToken() public {
        balanceOf[msg.sender] = totalSupply;
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);   
        balanceOf[msg.sender] -= _value;            
        totalSupply -= _value;                      
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        Burn(_from, _value);
        return true;
    }
}
contract BitGuildAccessAdmin {
    address public owner;
    address[] public operators;
    uint public MAX_OPS = 20; 
    mapping(address => bool) public isOperator;
    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );
    event OperatorAdded(address operator);
    event OperatorRemoved(address operator);
    constructor() public {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier onlyOperator() {
        require(
            isOperator[msg.sender] || msg.sender == owner,
            "Permission denied. Must be an operator or the owner."
        );
        _;
    }
    function transferOwnership(address _newOwner) public onlyOwner {
        require(
            _newOwner != address(0),
            "Invalid new owner address."
        );
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }
    function addOperator(address _newOperator) public onlyOwner {
        require(
            _newOperator != address(0),
            "Invalid new operator address."
        );
        require(
            !isOperator[_newOperator],
            "New operator exists."
        );
        require(
            operators.length < MAX_OPS,
            "Overflow."
        );
        operators.push(_newOperator);
        isOperator[_newOperator] = true;
        emit OperatorAdded(_newOperator);
    }
    function removeOperator(address _operator) public onlyOwner {
        require(
            operators.length > 0,
            "No operator."
        );
        require(
            isOperator[_operator],
            "Not an operator."
        );
        address lastOperator = operators[operators.length - 1];
        for (uint i = 0; i < operators.length; i++) {
            if (operators[i] == _operator) {
                operators[i] = lastOperator;
            }
        }
        operators.length -= 1; 
        isOperator[_operator] = false;
        emit OperatorRemoved(_operator);
    }
    function removeAllOps() public onlyOwner {
        for (uint i = 0; i < operators.length; i++) {
            isOperator[operators[i]] = false;
        }
        operators.length = 0;
    }
}
contract BitGuildWhitelist is BitGuildAccessAdmin {
    uint public total = 0;
    mapping (address => bool) public isWhitelisted;
    event AddressWhitelisted(address indexed addr, address operator);
    event AddressRemovedFromWhitelist(address indexed addr, address operator);
    modifier onlyWhitelisted(address _address) {
        require(
            isWhitelisted[_address],
            "Address is not on the whitelist."
        );
        _;
    }
    function () external payable {
        revert();
    }
    function addToWhitelist(address _newAddr) public onlyOperator {
        require(
            _newAddr != address(0),
            "Invalid new address."
        );
        require(
            !isWhitelisted[_newAddr],
            "Address is already whitelisted."
        );
        isWhitelisted[_newAddr] = true;
        total++;
        emit AddressWhitelisted(_newAddr, msg.sender);
    }
    function removeFromWhitelist(address _addr) public onlyOperator {
        require(
            _addr != address(0),
            "Invalid address."
        );
        require(
            isWhitelisted[_addr],
            "Address not in whitelist."
        );
        isWhitelisted[_addr] = false;
        if (total > 0) {
            total--;
        }
        emit AddressRemovedFromWhitelist(_addr, msg.sender);
    }
    function whitelistAddresses(address[] _addresses, bool _whitelisted) public onlyOperator {
        for (uint i = 0; i < _addresses.length; i++) {
            address addr = _addresses[i];
            if (isWhitelisted[addr] == _whitelisted) continue;
            if (_whitelisted) {
                addToWhitelist(addr);
            } else {
                removeFromWhitelist(addr);
            }
        }
    }
}
contract BitGuildFeeProvider is BitGuildAccessAdmin {
    uint constant NO_FEE = 10000;
    uint defaultPercentFee = 500; 
    mapping(bytes32 => uint) public customFee;  
    event LogFeeChanged(uint newPercentFee, uint oldPercentFee, address operator);
    event LogCustomFeeChanged(uint newPercentFee, uint oldPercentFee, address buyer, address seller, address token, address operator);
    function () external payable {
        revert();
    }
    function updateFee(uint _newFee) public onlyOperator {
        require(_newFee >= 0 && _newFee <= 10000, "Invalid percent fee.");
        uint oldPercentFee = defaultPercentFee;
        defaultPercentFee = _newFee;
        emit LogFeeChanged(_newFee, oldPercentFee, msg.sender);
    }
    function updateCustomFee(uint _newFee, address _currency, address _buyer, address _seller, address _token) public onlyOperator {
        require(_newFee >= 0 && _newFee <= 10000, "Invalid percent fee.");
        bytes32 key = _getHash(_currency, _buyer, _seller, _token);
        uint oldPercentFee = customFee[key];
        customFee[key] = _newFee;
        emit LogCustomFeeChanged(_newFee, oldPercentFee, _buyer, _seller, _token, msg.sender);
    }
    function getFee(uint _price, address _currency, address _buyer, address _seller, address _token) public view returns(uint percent, uint fee) {
        bytes32 key = _getHash(_currency, _buyer, _seller, _token);
        uint customPercentFee = customFee[key];
        (percent, fee) = _getFee(_price, customPercentFee);
    }
    function _getFee(uint _price, uint _percentFee) internal view returns(uint percent, uint fee) {
        require(_price >= 0, "Invalid price.");
        percent = _percentFee;
        if (_percentFee == 0) {
            percent = defaultPercentFee;
        }
        if (_percentFee == NO_FEE) {
            percent = 0;
            fee = 0;
        } else {
            fee = _safeMul(_price, percent) / 10000; 
        }
    }
    function _getHash(address _currency, address _buyer, address _seller, address _token) internal pure returns(bytes32 key) {
        key = keccak256(abi.encodePacked(_currency, _buyer, _seller, _token));
    }
    function _safeMul(uint a, uint b) internal pure returns (uint) {
        if (a == 0) {
            return 0;
        }
        uint c = a * b;
        assert(c / a == b);
        return c;
    }
}
pragma solidity ^0.4.24;
interface ERC721  {
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
    function balanceOf(address _owner) external view returns (uint256);
    function ownerOf(uint256 _tokenId) external view returns (address);
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) external;
    function safeTransferFrom(address _from, address _to, uint256 _tokenId) external;
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function approve(address _approved, uint256 _tokenId) external;
    function setApprovalForAll(address _operator, bool _approved) external;
    function getApproved(uint256 _tokenId) external view returns (address);
    function isApprovedForAll(address _owner, address _operator) external view returns (bool);
}
interface ERC721TokenReceiver {
	function onERC721Received(address _from, uint256 _tokenId, bytes data) external returns(bytes4);
	function onERC721Received(address _operator, address _from, uint256 _tokenId, bytes data) external returns(bytes4);
}
contract BitGuildMarketplace is BitGuildAccessAdmin {
    bytes4 constant ERC721_RECEIVED_OLD = 0xf0b9e5ba;
    bytes4 constant ERC721_RECEIVED = 0x150b7a02;
    BitGuildToken public PLAT = BitGuildToken(0x7E43581b19ab509BCF9397a2eFd1ab10233f27dE); 
    BitGuildWhitelist public Whitelist = BitGuildWhitelist(0xA8CedD578fed14f07C3737bF42AD6f04FAAE3978); 
    BitGuildFeeProvider public FeeProvider = BitGuildFeeProvider(0x58D36571250D91eF5CE90869E66Cd553785364a2); 
    uint public defaultExpiry = 7 days;  
    enum Currency { PLAT, ETH }
    struct Listing {
        Currency currency;      
        address seller;         
        address token;          
        uint tokenId;           
        uint price;             
        uint createdAt;         
        uint expiry;            
    }
    mapping(bytes32 => Listing) public listings;
    event LogListingCreated(address _seller, address _contract, uint _tokenId, uint _createdAt, uint _expiry);
    event LogListingExtended(address _seller, address _contract, uint _tokenId, uint _createdAt, uint _expiry);
    event LogItemSold(address _buyer, address _seller, address _contract, uint _tokenId, uint _price, Currency _currency, uint _soldAt);
    event LogItemWithdrawn(address _seller, address _contract, uint _tokenId, uint _withdrawnAt);
    event LogItemExtended(address _contract, uint _tokenId, uint _modifiedAt, uint _expiry);
    modifier onlyWhitelisted(address _contract) {
        require(Whitelist.isWhitelisted(_contract), "Contract not in whitelist.");
        _;
    }
    function () external payable {
        revert();
    }
    function getHashKey(address _contract, uint _tokenId) public pure returns(bytes32 key) {
        key = _getHashKey(_contract, _tokenId);
    }
    function getFee(uint _price, address _currency, address _buyer, address _seller, address _token) public view returns(uint percent, uint fee) {
        (percent, fee) = FeeProvider.getFee(_price, _currency, _buyer, _seller, _token);
    }
    function onERC721Received(address _from, uint _tokenId, bytes _extraData) external returns(bytes4) {
        _deposit(_from, msg.sender, _tokenId, _extraData);
        return ERC721_RECEIVED_OLD;
    }
    function onERC721Received(address _operator, address _from, uint _tokenId, bytes _extraData) external returns(bytes4) {
        _deposit(_from, msg.sender, _tokenId, _extraData);
        return ERC721_RECEIVED;
    }
    function extendItem(address _contract, uint _tokenId) public onlyWhitelisted(_contract) returns(bool) {
        bytes32 key = _getHashKey(_contract, _tokenId);
        address seller = listings[key].seller;
        require(seller == msg.sender, "Only seller can extend listing.");
        require(listings[key].expiry > 0, "Item not listed.");
        listings[key].expiry = now + defaultExpiry;
        emit LogListingExtended(seller, _contract, _tokenId, listings[key].createdAt, listings[key].expiry);
        return true;
    }
    function withdrawItem(address _contract, uint _tokenId) public onlyWhitelisted(_contract) {
        bytes32 key = _getHashKey(_contract, _tokenId);
        address seller = listings[key].seller;
        require(seller == msg.sender, "Only seller can withdraw listing.");
        ERC721 gameToken = ERC721(_contract);
        gameToken.safeTransferFrom(this, seller, _tokenId);
        emit LogItemWithdrawn(seller, _contract, _tokenId, now);
        delete(listings[key]);
    }
    function buyWithETH(address _token, uint _tokenId) public onlyWhitelisted(_token) payable {
        _buy(_token, _tokenId, Currency.ETH, msg.value, msg.sender);
    }
    function receiveApproval(address _buyer, uint _value, BitGuildToken _PLAT, bytes _extraData) public {
        require(_extraData.length > 0, "No extraData provided.");
        require(msg.sender == address(PLAT), "Unauthorized PLAT contract address.");
        address token;
        uint tokenId;
        (token, tokenId) = _decodeBuyData(_extraData);
        _buy(token, tokenId, Currency.PLAT, _value, _buyer);
    }
    function updateFeeProvider(address _newAddr) public onlyOperator {
        require(_newAddr != address(0), "Invalid contract address.");
        FeeProvider = BitGuildFeeProvider(_newAddr);
    }
    function updateWhitelist(address _newAddr) public onlyOperator {
        require(_newAddr != address(0), "Invalid contract address.");
        Whitelist = BitGuildWhitelist(_newAddr);
    }
    function updateExpiry(uint _days) public onlyOperator {
        require(_days > 0, "Invalid number of days.");
        defaultExpiry = _days * 1 days;
    }
    function withdrawETH() public onlyOwner payable {
        msg.sender.transfer(msg.value);
    }
    function withdrawPLAT() public onlyOwner payable {
        uint balance = PLAT.balanceOf(this);
        PLAT.transfer(msg.sender, balance);
    }
    function _getHashKey(address _contract, uint _tokenId) internal pure returns(bytes32 key) {
        key = keccak256(abi.encodePacked(_contract, _tokenId));
    }
    function _newListing(address _seller, address _contract, uint _tokenId, uint _price, Currency _currency) internal {
        bytes32 key = _getHashKey(_contract, _tokenId);
        uint createdAt = now;
        uint expiry = now + defaultExpiry;
        listings[key].currency = _currency;
        listings[key].seller = _seller;
        listings[key].token = _contract;
        listings[key].tokenId = _tokenId;
        listings[key].price = _price;
        listings[key].createdAt = createdAt;
        listings[key].expiry = expiry;
        emit LogListingCreated(_seller, _contract, _tokenId, createdAt, expiry);
    }
    function _deposit(address _seller, address _contract, uint _tokenId, bytes _extraData) internal onlyWhitelisted(_contract) {
        uint price;
        uint currencyUint;
        (currencyUint, price) = _decodePriceData(_extraData);
        Currency currency = Currency(currencyUint);
        require(price > 0, "Invalid price.");
        _newListing(_seller, _contract, _tokenId, price, currency);
    }
    function _buy(address _token, uint _tokenId, Currency _currency, uint _price, address _buyer) internal {
        bytes32 key = _getHashKey(_token, _tokenId);
        Currency currency = listings[key].currency;
        address seller = listings[key].seller;
        address currencyAddress = _currency == Currency.PLAT ? address(PLAT) : address(0);
        require(currency == _currency, "Wrong currency.");
        require(_price > 0 && _price == listings[key].price, "Invalid price.");
        require(listings[key].expiry > now, "Item expired.");
        ERC721 gameToken = ERC721(_token);
        require(gameToken.ownerOf(_tokenId) == address(this), "Item is not available.");
        if (_currency == Currency.PLAT) {
            require(PLAT.transferFrom(_buyer, address(this), _price), "PLAT payment transfer failed.");
        }
        gameToken.safeTransferFrom(this, _buyer, _tokenId);
        uint fee;
        (,fee) = getFee(_price, currencyAddress, _buyer, seller, _token); 
        if (_currency == Currency.PLAT) {
            PLAT.transfer(seller, _price - fee);
        } else {
            require(seller.send(_price - fee) == true, "Transfer to seller failed.");
        }
        emit LogItemSold(_buyer, seller, _token, _tokenId, _price, currency, now);
        delete(listings[key]);
    }
    function _decodePriceData(bytes _extraData) internal pure returns(uint _currency, uint _price) {
        uint256 offset = 64;
        _price = _bytesToUint256(offset, _extraData);
        offset -= 32;
        _currency = _bytesToUint256(offset, _extraData);
    }
    function _decodeBuyData(bytes _extraData) internal pure returns(address _contract, uint _tokenId) {
        uint256 offset = 64;
        _tokenId = _bytesToUint256(offset, _extraData);
        offset -= 32;
        _contract = _bytesToAddress(offset, _extraData);
    }
    function _bytesToUint256(uint _offst, bytes memory _input) internal pure returns (uint256 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function _bytesToAddress(uint _offst, bytes memory _input) internal pure returns (address _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
}
```

## RQ1_1064e887af8d

SHA-256 `f9addd455e43a4f20f212e19f1eee7d4775b3015d4c04699e0325cc3fd1ec07c`

```solidity
pragma solidity ^0.4.11;
library SafeMath {
  function mul(uint a, uint b) internal returns (uint) {
    uint c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint a, uint b) internal returns (uint) {
    uint c = a / b;
    return c;
  }
  function sub(uint a, uint b) internal returns (uint) {
    assert(b <= a);
    return a - b;
  }
  function add(uint a, uint b) internal returns (uint) {
    uint c = a + b;
    assert(c >= a);
    return c;
  }
  function max64(uint64 a, uint64 b) internal constant returns (uint64) {
    return a >= b ? a : b;
  }
  function min64(uint64 a, uint64 b) internal constant returns (uint64) {
    return a < b ? a : b;
  }
  function max256(uint256 a, uint256 b) internal constant returns (uint256) {
    return a >= b ? a : b;
  }
  function min256(uint256 a, uint256 b) internal constant returns (uint256) {
    return a < b ? a : b;
  }
  function assert(bool assertion) internal {
    if (!assertion) {
      throw;
    }
  }
}
contract ERC20Basic {
  uint public totalSupply;
  function balanceOf(address who) constant returns (uint);
  function transfer(address to, uint value);
  event Transfer(address indexed from, address indexed to, uint value);
}
contract DestoryBasic {
    address destoryAddress;
    function setDestoryAddress(address _destory) {
        destoryAddress = _destory;
    }
    function ifDestory(address from) returns (bool) {
        if (from == destoryAddress) {
            return true;
        }
        return false;
    }
}
contract BasicToken is ERC20Basic,DestoryBasic {
  using SafeMath for uint;
  mapping(address => uint) balances;
  modifier onlyPayloadSize(uint size) {
     if(msg.data.length < size + 4) {
       throw;
     }
     _;
  }
  function transfer(address _to, uint _value) onlyPayloadSize(2 * 32) {
    if(ifDestory(msg.sender)) throw;
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
  }
  function balanceOf(address _owner) constant returns (uint balance) {
    return balances[_owner];
  }
}
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) constant returns (uint);
  function transferFrom(address from, address to, uint value);
  function approve(address spender, uint value);
  event Approval(address indexed owner, address indexed spender, uint value);
}
contract StandardToken is BasicToken, ERC20 {
  mapping (address => mapping (address => uint)) allowed;
  function transferFrom(address _from, address _to, uint _value) onlyPayloadSize(3 * 32) {
    if(ifDestory(msg.sender)) throw;
    var _allowance = allowed[_from][msg.sender];
    balances[_to] = balances[_to].add(_value);
    balances[_from] = balances[_from].sub(_value);
    allowed[_from][msg.sender] = _allowance.sub(_value);
    Transfer(_from, _to, _value);
  }
  function approve(address _spender, uint _value) {
    if ((_value != 0) && (allowed[msg.sender][_spender] != 0)) throw ;
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
  }
  function allowance(address _owner, address _spender) constant returns (uint remaining) {
    return allowed[_owner][_spender];
  }
}
contract Ownable {
  address public owner;
  modifier onlyOwner() {
    if (msg.sender != owner) {
      throw;
    }
    _;
  }
  function transferOwnership(address newOwner) onlyOwner {
    if (newOwner != address(0)) {
      owner = newOwner;
    }
  }
}
contract GTSTOKEN is StandardToken,Ownable {
  using SafeMath for uint;
  string public name = "GTSTOKEN";
  string public symbol = "GTS";
  uint public decimals = 9;
  uint public totalSupply = 10000000000 * (10 ** decimals);
  uint lockTotal = 4000000000 * (10 ** decimals);
  uint public releaseTotal = 500000000 * (10 ** decimals);
  uint lockTime = 0;
  function GTSTOKEN (address admin_) {
      lockTime = 1518192000;
      owner = admin_;
      setDestoryAddress(address(0x0));
      balances[admin_] = totalSupply - lockTotal;
  }
  function release() onlyOwner {
      if (lockTime + 1 years > now) {
          throw;
      }
      if ( lockTotal == 0 ) {
        throw;
      }
      lockTotal = lockTotal.sub(releaseTotal);
      balances[owner] = balances[owner].add(releaseTotal);
      lockTime = lockTime + 1 years;
      return;
  }
}
```

## RQ1_a3fa5876304e

SHA-256 `2389f2367658d1dd09cbba21ab981df89090389985a84db7ce2f1fab8fc116de`

```solidity
pragma solidity ^ 0.4.18;
contract Etherumble {
    struct PlayerBets {
        address addPlayer;
        uint amount;
    }
    PlayerBets[] users;
    address[] players = new address[](20);
    uint[] bets = new uint[](20);
    uint nbUsers = 0;
    uint totalBets = 0;
    uint fees = 0;
    uint endBlock = 0;
    address owner;
    address lastWinner;
    uint lastWinnerTicket=0;
    uint totalGames = 0;
    modifier isOwner() {
        require(msg.sender == owner);
        _;
    }
    modifier hasValue() {
        require(msg.value >= 10000000000000000 && nbUsers < 19); 
        _;
    }
    modifier onlyIf(bool _condition) {
        require(_condition);
        _;
    }
    function Lottery() public {
        owner = msg.sender;
    }
    function getActivePlayers() public constant returns(uint) {
        return nbUsers;
    }
    function getPlayerAddress(uint index) public constant returns(address) {
        return players[index];
    }
    function getPlayerBet(uint index) public constant returns(uint) {
        return bets[index];
    }
    function getEndBlock() public constant returns(uint) {
        return endBlock;
    }
    function getLastWinner() public constant returns(address) {
        return lastWinner;
    }
    function getLastWinnerTicket() public constant returns(uint) {
        return lastWinnerTicket;
    }
    function getTotalGames() public constant returns(uint) {
        return totalGames;
    }
    function() public payable hasValue {
        checkinter();
        players[nbUsers] = msg.sender;
        bets[nbUsers] = msg.value;
        users.push(PlayerBets(msg.sender, msg.value));
        nbUsers++;
        totalBets += msg.value;
        if (nbUsers == 2) { 
            endBlock = block.number + 15;
        }
    }
    function endLottery() internal {
        uint sum = 0;
        uint winningNumber = uint(block.blockhash(block.number - 1)) % totalBets;
        for (uint i = 0; i < nbUsers; i++) {
            sum += users[i].amount;
            if (sum >= winningNumber) {
                withrawWin(users[i].addPlayer,winningNumber);
                return;
            }
        }
    }
    function withrawWin(address winner,uint winticket) internal {
        uint tempTot = totalBets;
        lastWinnerTicket = winticket;
        totalGames++;
        nbUsers = 0;
        totalBets = 0;
        endBlock = 0;
        delete users;
        fees += tempTot * 5 / 100;
        winner.transfer(tempTot * 95 / 100);
        lastWinner = winner;
    }
    function withrawFee() public isOwner {
        owner.transfer(fees);
        fees = 0;
    }
    function destroykill() public isOwner {
        selfdestruct(owner);
    }
    function checkinter() internal{ 
        if (endBlock <= block.number && endBlock != 0) {
            endLottery();
        }
    }
    function callback() public isOwner{ 
        if (endBlock <= block.number && endBlock != 0) {
            endLottery();
        }
    }
}
```

## RQ1_78c8c287484a

SHA-256 `f7283078ca4ca4bb14d35aeab0c9ef2e9db633d155e2d5f1f0cdb8bb927922de`

```solidity
pragma solidity ^0.4.24;
contract TeikhosBounty {
    bytes32 proof_of_public_key1 = hex"94cd5137c63cf80cdd176a2a6285572cc076f2fbea67c8b36e65065be7bc34ec";
    bytes32 proof_of_public_key2 = hex"9f6463aadf1a8aed68b99aa14538f16d67bf586a4bdecb904d56d5edb2cfb13a";
    function authenticate(bytes _publicKey) returns (bool) { 
        address signer = address(keccak256(_publicKey));
        bytes32 publicKey1;
        bytes32 publicKey2;
        assembly {
        publicKey1 := mload(add(_publicKey,0x20))
        publicKey2 := mload(add(_publicKey,0x40))
        }
        bytes32 r = proof_of_public_key1 ^ publicKey1;
        bytes32 s = proof_of_public_key2 ^ publicKey2;
        bytes32 msgHash = keccak256("\x19Ethereum Signed Message:\n64", _publicKey);
        if(ecrecover(msgHash, 27, r, s) == signer) suicide(msg.sender);
        if(ecrecover(msgHash, 28, r, s) == signer) suicide(msg.sender);
    }
    function() payable {}                            
}

```

## RQ1_d5000081f440

SHA-256 `6c21957e96b51fa3b4d78ce0cfc989eaa7277299488ad329a27285a3a751c07f`

```solidity
pragma solidity ^0.4.18;
contract DogCoreInterface {
    address public ceoAddress;
    address public cfoAddress;
    function getDog(uint256 _id)
        external
        view
        returns (
        uint256 cooldownIndex,
        uint256 nextActionAt,
        uint256 siringWithId,
        uint256 birthTime,
        uint256 matronId,
        uint256 sireId,
        uint256 generation,
        uint256 genes,
        uint8  variation,
        uint256 gen0
    );
    function ownerOf(uint256 _tokenId) external view returns (address);
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function sendMoney(address _to, uint256 _money) external;
    function totalSupply() external view returns (uint);
}
contract LotteryBase {
    uint8 public currentGene;
    uint256 public lastBlockNumber;
    uint256 randomSeed = 1;
    address public bonusPool;
    struct CLottery {
        uint8[7]        luckyGenes;
        uint256         totalAmount;
        uint256         openBlock;
        bool            isReward;
        bool         noFirstReward;
    }
    CLottery[] public CLotteries;
    address public finalLottery;
    uint256 public SpoolAmount = 0;
    DogCoreInterface public dogCore;
    event OpenLottery(uint8 currentGene, uint8 luckyGenes, uint256 currentTerm, uint256 blockNumber, uint256 totalAmount);
    event OpenCarousel(uint256 luckyGenes, uint256 currentTerm, uint256 blockNumber, uint256 totalAmount);
    modifier onlyCEO() {
        require(msg.sender == dogCore.ceoAddress());
        _;  
    }
    modifier onlyCFO() {
        require(msg.sender == dogCore.cfoAddress());
        _;  
    }
    function toLotteryPool(uint amount) public onlyCFO {
        require(SpoolAmount >= amount);
        SpoolAmount -= amount;
    }
    function _isCarousal(uint256 currentTerm) external view returns(bool) {
       return (currentTerm > 1 && CLotteries[currentTerm - 2].noFirstReward && CLotteries[currentTerm - 1].noFirstReward); 
    }
    function getCurrentTerm() external view returns (uint256) {
        return (CLotteries.length - 1);
    }
}
contract LotteryGenes is LotteryBase {
    function convertGeneArray(uint256 gene) public pure returns(uint8[7]) {
        uint8[28] memory geneArray; 
        uint8[7] memory lotteryArray;
        uint index = 0;
        for (index = 0; index < 28; index++) {
            uint256 geneItem = gene % (2 ** (5 * (index + 1)));
            geneItem /= (2 ** (5 * index));
            geneArray[index] = uint8(geneItem);
        }
        for (index = 0; index < 7; index++) {
            uint size = 4 * index;
            lotteryArray[index] = geneArray[size];
        }
        return lotteryArray;
    }
    function convertGene(uint8[7] luckyGenes) public pure returns(uint256) {
        uint8[28] memory geneArray;
        for (uint8 i = 0; i < 28; i++) {
            if (i%4 == 0) {
                geneArray[i] = luckyGenes[i/4];
            } else {
                geneArray[i] = 6;
            }
        }
        uint256 gene = uint256(geneArray[0]);
        for (uint8 index = 1; index < 28; index++) {
            uint256 geneItem = uint256(geneArray[index]);
            gene += geneItem << (index * 5);
        }
        return gene;
    }
}
contract SetLottery is LotteryGenes {
    function random(uint8 seed) internal returns(uint8) {
        randomSeed = block.timestamp;
        return uint8(uint256(keccak256(randomSeed, block.difficulty))%seed)+1;
    }
    function openLottery(uint8 _viewId) public returns(uint8,uint8) {
        uint8 viewId = _viewId;
        require(viewId < 7);
        uint256 currentTerm = CLotteries.length - 1;
        CLottery storage clottery = CLotteries[currentTerm];
        if (currentGene == 0 && clottery.openBlock > 0 && clottery.isReward == false) {
            OpenLottery(viewId, clottery.luckyGenes[viewId], currentTerm, 0, 0);
            return (clottery.luckyGenes[viewId],1);
        }
        if (lastBlockNumber == block.number) {
            OpenLottery(viewId, clottery.luckyGenes[viewId], currentTerm, 0, 0);
            return (clottery.luckyGenes[viewId],2);
        }
        if (currentGene == 0 && clottery.isReward == true) {
            CLottery memory _clottery;
            _clottery.luckyGenes = [0,0,0,0,0,0,0];
            _clottery.totalAmount = uint256(0);
            _clottery.isReward = false;
            _clottery.openBlock = uint256(0);
            currentTerm = CLotteries.push(_clottery) - 1;
        }
        if (this._isCarousal(currentTerm)) {
            revert();
        }
        uint8 luckyNum = 0;
        if (currentGene == 6) {
            if (bonusPool.balance <= SpoolAmount) {
                OpenLottery(viewId, clottery.luckyGenes[viewId], currentTerm, 0, 0);
                return (clottery.luckyGenes[viewId],3);
            }
            luckyNum = random(8);
            CLotteries[currentTerm].luckyGenes[currentGene] = luckyNum;
            OpenLottery(currentGene, luckyNum, currentTerm, block.number, bonusPool.balance);
            currentGene = 0;
            CLotteries[currentTerm].openBlock = block.number;
            CLotteries[currentTerm].totalAmount = bonusPool.balance;
            lastBlockNumber = block.number;
        } else { 
            luckyNum = random(12);
            CLotteries[currentTerm].luckyGenes[currentGene] = luckyNum;
            OpenLottery(currentGene, luckyNum, currentTerm, 0, 0);
            currentGene ++;
            lastBlockNumber = block.number;
        }
        return (luckyNum,0);
    } 
    function random2() internal view returns (uint256) {
        return uint256(uint256(keccak256(block.timestamp, block.difficulty))%uint256(dogCore.totalSupply()) + 1);
    }
    function openCarousel() public {
        uint256 currentTerm = CLotteries.length - 1;
        CLottery storage clottery = CLotteries[currentTerm];
        if (currentGene == 0 && clottery.openBlock > 0 && clottery.isReward == false) {
            OpenCarousel(convertGene(clottery.luckyGenes), currentTerm, clottery.openBlock, clottery.totalAmount);
        }
        if (currentGene == 0 && clottery.openBlock > 0 && clottery.isReward == true) {
            CLottery memory _clottery;
            _clottery.luckyGenes = [0,0,0,0,0,0,0];
            _clottery.totalAmount = uint256(0);
            _clottery.isReward = false;
            _clottery.openBlock = uint256(0);
            currentTerm = CLotteries.push(_clottery) - 1;
        }
        require (this._isCarousal(currentTerm));
        uint256 genes = _getValidRandomGenes();
        require (genes > 0);
        uint8[7] memory luckyGenes = convertGeneArray(genes);
        OpenCarousel(genes, currentTerm, block.number, bonusPool.balance);
        CLotteries[currentTerm].luckyGenes = luckyGenes;
        CLotteries[currentTerm].openBlock = block.number;
        CLotteries[currentTerm].totalAmount = bonusPool.balance;
    }
    function _getValidRandomGenes() internal view returns (uint256) {
        uint256 luckyDog = random2();
        uint256 genes = _validGenes(luckyDog);
        uint256 totalSupply = dogCore.totalSupply();
        if (genes > 0) {
            return genes;
        }  
        uint256 min = (luckyDog < totalSupply-luckyDog) ? (luckyDog - 1) : totalSupply-luckyDog;
        for (uint256 i = 1; i < min + 1; i++) {
            genes = _validGenes(luckyDog - i);
            if (genes > 0) {
                break;
            }
            genes = _validGenes(luckyDog + i);
            if (genes > 0) {
                    break;
                }
            }
        if (genes == 0) {
            if (min == luckyDog - 1) {
                for (i = min + luckyDog; i < totalSupply + 1; i++) {
                        genes = _validGenes(i);
                        if (genes > 0) {
                            break;
                        }
                    }   
                }
            if (min == totalSupply - luckyDog) {
                for (i = min; i < luckyDog; i++) {
                        genes = _validGenes(luckyDog - i - 1);
                        if (genes > 0) {
                            break;
                        }
                    }   
                }
            }
        return genes;
    }
    function _validGenes(uint256 dogId) internal view returns (uint256) {
        var(, , , , , ,generation, genes, variation,) = dogCore.getDog(dogId);
        if (generation == 0 || dogCore.ownerOf(dogId) == finalLottery || variation > 0) {
            return 0;
        } else {
            return genes;
        }
    }
}
contract LotteryCore is SetLottery {
    function LotteryCore(address _ktAddress) public {
        bonusPool = _ktAddress;
        dogCore = DogCoreInterface(_ktAddress);
        CLottery memory _clottery;
        _clottery.luckyGenes = [0,0,0,0,0,0,0];
        _clottery.totalAmount = uint256(0);
        _clottery.isReward = false;
        _clottery.openBlock = uint256(0);
        CLotteries.push(_clottery);
    }
    function setFinalLotteryAddress(address _flAddress) public onlyCEO {
        finalLottery = _flAddress;
    }
    function getCLottery() 
        public 
        view 
        returns (
            uint8[7]        luckyGenes,
            uint256         totalAmount,
            uint256         openBlock,
            bool            isReward,
            uint256         term
        ) {
            term = CLotteries.length - uint256(1);
            luckyGenes = CLotteries[term].luckyGenes;
            totalAmount = CLotteries[term].totalAmount;
            openBlock = CLotteries[term].openBlock;
            isReward = CLotteries[term].isReward;
    }
    function rewardLottery(bool isMore) external {
        require(msg.sender == finalLottery);
        uint256 term = CLotteries.length - 1;
        CLotteries[term].isReward = true;
        CLotteries[term].noFirstReward = isMore;
    }
    function toSPool(uint amount) external {
        require(msg.sender == finalLottery);
        SpoolAmount += amount;
    }
}
contract FinalLottery {
    bool public isLottery = true;
    LotteryCore lotteryCore;
    DogCoreInterface dogCore;
    uint8[7] public luckyGenes;
    uint256         totalAmount;
    uint256         openBlock;
    bool            isReward;
    uint256         currentTerm;
    uint256  public duration;
    uint8   public  lotteryRatio;
    uint8[7] public lotteryParam;
    uint8   public  carousalRatio;
    uint8[7] public carousalParam; 
    struct FLottery {
        address[]        owners0;
        uint256[]        dogs0;
        address[]        owners1;
        uint256[]        dogs1;
        address[]        owners2;
        uint256[]        dogs2;
        address[]        owners3;
        uint256[]        dogs3;
        address[]        owners4;
        uint256[]        dogs4;
        address[]        owners5;
        uint256[]        dogs5;
        address[]        owners6;
        uint256[]        dogs6;
        uint256[]       reward;
    }
    mapping(uint256 => FLottery) flotteries;
    function FinalLottery(address _lcAddress) public {
        lotteryCore = LotteryCore(_lcAddress);
        dogCore = DogCoreInterface(lotteryCore.bonusPool());
        duration = 11520;
        lotteryRatio = 23;
        lotteryParam = [46,16,10,9,8,6,5];
        carousalRatio = 12;
        carousalParam = [35,18,14,12,8,7,6];
    }
    event DistributeLottery(uint256[] rewardArray, uint256 currentTerm);
    event RegisterLottery(uint256 dogId, address owner, uint8 lotteryClass, string result);
    function setLotteryDuration(uint256 durationBlocks) public {
        require(msg.sender == dogCore.ceoAddress());
        require(durationBlocks > 140);
        require(durationBlocks < block.number);
        duration = durationBlocks;
    }
    function registerLottery(uint256 dogId) public returns (uint8) {
        uint256 _dogId = dogId;
        (luckyGenes, totalAmount, openBlock, isReward, currentTerm) = lotteryCore.getCLottery();
        address owner = dogCore.ownerOf(_dogId);
        require (owner != address(this));
        require(address(dogCore) == msg.sender);
        require(totalAmount > 0 && isReward == false && openBlock > (block.number-duration));
        var(, , , birthTime, , ,generation,genes, variation,) = dogCore.getDog(_dogId);
        require(birthTime < openBlock);
        require(generation > 0);
        require(variation == 0);
        uint8 _lotteryClass = getLotteryClass(luckyGenes, genes);
        require(_lotteryClass < 7);
        address[] memory owners;
        uint256[] memory dogs;
         (dogs, owners) = _getLuckyList(currentTerm, _lotteryClass);
        for (uint i = 0; i < dogs.length; i++) {
            if (_dogId == dogs[i]) {
                RegisterLottery(_dogId, owner, _lotteryClass,"dog already registered");
                 return 5;
            }
        }
        _pushLuckyInfo(currentTerm, _lotteryClass, owner, _dogId);
        RegisterLottery(_dogId, owner, _lotteryClass,"successful");
        return 0;
    }
    function distributeLottery() public returns (uint8) {
        (luckyGenes, totalAmount, openBlock, isReward, currentTerm) = lotteryCore.getCLottery();
        require(openBlock > 0 && openBlock < (block.number-duration));
        require(totalAmount >= lotteryCore.SpoolAmount());
        if (isReward == true) {
            DistributeLottery(flotteries[currentTerm].reward, currentTerm);
            return 1;
        }
        uint256 legalAmount = totalAmount - lotteryCore.SpoolAmount();
        uint256 totalDistribute = 0;
        uint8[7] memory lR;
        uint8 ratio;
        if (lotteryCore._isCarousal(currentTerm) ) {
            lR = carousalParam;
            ratio = carousalRatio;
        } else {
            lR = lotteryParam;
            ratio = lotteryRatio;
        }
        for (uint8 i = 0; i < 7; i++) {
            address[] memory owners;
            uint256[] memory dogs;
            (dogs, owners) = _getLuckyList(currentTerm, i);
            if (owners.length > 0) {
                    uint256 reward = (legalAmount * ratio * lR[i])/(10000 * owners.length);
                    totalDistribute += reward * owners.length;
                    dogCore.sendMoney(dogCore.cfoAddress(),reward * owners.length/10);
                    for (uint j = 0; j < owners.length; j++) {
                        address gen0Add;
                        if (i == 0) {
                            dogCore.sendMoney(owners[j],reward*95*9/1000);
                            gen0Add = _getGen0Address(dogs[j]);
                            assert(gen0Add != address(0));
                            dogCore.sendMoney(gen0Add,reward*5/100);
                        } else if (i == 1) {
                            dogCore.sendMoney(owners[j],reward*97*9/1000);
                            gen0Add = _getGen0Address(dogs[j]);
                            assert(gen0Add != address(0));
                            dogCore.sendMoney(gen0Add,reward*3/100);
                        } else if (i == 2) {
                            dogCore.sendMoney(owners[j],reward*98*9/1000);
                            gen0Add = _getGen0Address(dogs[j]);
                            assert(gen0Add != address(0));
                            dogCore.sendMoney(gen0Add,reward*2/100);
                        } else {
                            dogCore.sendMoney(owners[j],reward*9/10);
                        }
                    }
                    flotteries[currentTerm].reward.push(reward);  
                } else {
                    flotteries[currentTerm].reward.push(0); 
                } 
        }
        if (flotteries[currentTerm].owners0.length == 0) {
            lotteryCore.toSPool((lotteryCore.bonusPool().balance - lotteryCore.SpoolAmount())/20);
            lotteryCore.rewardLottery(true);
        } else {
            lotteryCore.rewardLottery(false);
        }
        DistributeLottery(flotteries[currentTerm].reward, currentTerm);
        return 0;
    }
    function _getGen0Address(uint256 dogId) internal view returns(address) {
        var(, , , , , , , , , gen0) = dogCore.getDog(dogId);
        return dogCore.ownerOf(gen0);
    }
    function _getLuckyList(uint256 currentTerm1, uint8 lotclass) public view returns (uint256[] kts, address[] ons) {
        if (lotclass==0) {
            ons = flotteries[currentTerm1].owners0;
            kts = flotteries[currentTerm1].dogs0;
        } else if (lotclass==1) {
            ons = flotteries[currentTerm1].owners1;
            kts = flotteries[currentTerm1].dogs1;
        } else if (lotclass==2) {
            ons = flotteries[currentTerm1].owners2;
            kts = flotteries[currentTerm1].dogs2;
        } else if (lotclass==3) {
            ons = flotteries[currentTerm1].owners3;
            kts = flotteries[currentTerm1].dogs3;
        } else if (lotclass==4) {
            ons = flotteries[currentTerm1].owners4;
            kts = flotteries[currentTerm1].dogs4;
        } else if (lotclass==5) {
            ons = flotteries[currentTerm1].owners5;
            kts = flotteries[currentTerm1].dogs5;
        } else if (lotclass==6) {
            ons = flotteries[currentTerm1].owners6;
            kts = flotteries[currentTerm1].dogs6;
        }
    }
    function _pushLuckyInfo(uint256 currentTerm1, uint8 _lotteryClass, address owner, uint256 _dogId) internal {
        if (_lotteryClass == 0) {
            flotteries[currentTerm1].owners0.push(owner);
            flotteries[currentTerm1].dogs0.push(_dogId);
        } else if (_lotteryClass == 1) {
            flotteries[currentTerm1].owners1.push(owner);
            flotteries[currentTerm1].dogs1.push(_dogId);
        } else if (_lotteryClass == 2) {
            flotteries[currentTerm1].owners2.push(owner);
            flotteries[currentTerm1].dogs2.push(_dogId);
        } else if (_lotteryClass == 3) {
            flotteries[currentTerm1].owners3.push(owner);
            flotteries[currentTerm1].dogs3.push(_dogId);
        } else if (_lotteryClass == 4) {
            flotteries[currentTerm1].owners4.push(owner);
            flotteries[currentTerm1].dogs4.push(_dogId);
        } else if (_lotteryClass == 5) {
            flotteries[currentTerm1].owners5.push(owner);
            flotteries[currentTerm1].dogs5.push(_dogId);
        } else if (_lotteryClass == 6) {
            flotteries[currentTerm1].owners6.push(owner);
            flotteries[currentTerm1].dogs6.push(_dogId);
        }
    }
    function getLotteryClass(uint8[7] luckyGenesArray, uint256 genes) internal view returns(uint8) {
        if (currentTerm < 0) {
            return 100;
        }
        uint8[7] memory dogArray = lotteryCore.convertGeneArray(genes);
        uint8 cnt = 0;
        uint8 lnt = 0;
        for (uint i = 0; i < 6; i++) {
            if (luckyGenesArray[i] > 0 && luckyGenesArray[i] == dogArray[i]) {
                cnt++;
            }
        }
        if (luckyGenesArray[6] > 0 && luckyGenesArray[6] == dogArray[6]) {
            lnt = 1;
        }
        uint8 lotclass = 100;
        if (cnt==6 && lnt==1) {
            lotclass = 0;
        } else if (cnt==6 && lnt==0) {
            lotclass = 1;
        } else if (cnt==5 && lnt==1) {
            lotclass = 2;
        } else if (cnt==5 && lnt==0) {
            lotclass = 3;
        } else if (cnt==4 && lnt==1) {
            lotclass = 4;
        } else if (cnt==3 && lnt==1) {
            lotclass = 5;
        } else if (cnt==3 && lnt==0) {
            lotclass = 6;
        } else {
            lotclass = 100;
        }
        return lotclass;
    }
    function checkLottery(uint256 genes) public view returns(uint8) {
        var(luckyGenesArray, , , isReward1, ) = lotteryCore.getCLottery();
        if (isReward1) {
            return 100;
        }
        return getLotteryClass(luckyGenesArray, genes);
    }
    function getCLottery() 
        public 
        view 
        returns (
            uint8[7]        luckyGenes1,
            uint256         totalAmount1,
            uint256         openBlock1,
            bool            isReward1,
            uint256         term1,
            uint8           currentGenes1,
            uint256         tSupply,
            uint256         sPoolAmount1,
            uint256[]       reward1
        ) {
            (luckyGenes1, totalAmount1, openBlock1, isReward1, term1) = lotteryCore.getCLottery();
            currentGenes1 = lotteryCore.currentGene();
            tSupply = dogCore.totalSupply();
            sPoolAmount1 = lotteryCore.SpoolAmount();
            reward1 = flotteries[term1].reward;
    }
}
```

## RQ1_1c4665aef927

SHA-256 `abec7b53afa1e7baa336c11404f036408f62f073926fbe15966742536d2fe750`

```solidity
pragma solidity >=0.5.4 <0.6.0;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes calldata _extraData) external; }
contract TheAO {
	address public theAO;
	address public nameTAOPositionAddress;
	mapping (address => bool) public whitelist;
	constructor() public {
		theAO = msg.sender;
	}
	modifier inWhitelist() {
		require (whitelist[msg.sender] == true);
		_;
	}
	function transferOwnership(address _theAO) public {
		require (msg.sender == theAO);
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public {
		require (msg.sender == theAO);
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
}
library SafeMath {
	function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
		if (a == 0) {
			return 0;
		}
		c = a * b;
		assert(c / a == b);
		return c;
	}
	function div(uint256 a, uint256 b) internal pure returns (uint256) {
		return a / b;
	}
	function sub(uint256 a, uint256 b) internal pure returns (uint256) {
		assert(b <= a);
		return a - b;
	}
	function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
		c = a + b;
		assert(c >= a);
		return c;
	}
}
interface INameTAOPosition {
	function senderIsAdvocate(address _sender, address _id) external view returns (bool);
	function senderIsListener(address _sender, address _id) external view returns (bool);
	function senderIsSpeaker(address _sender, address _id) external view returns (bool);
	function senderIsPosition(address _sender, address _id) external view returns (bool);
	function getAdvocate(address _id) external view returns (address);
	function nameIsAdvocate(address _nameId, address _id) external view returns (bool);
	function nameIsPosition(address _nameId, address _id) external view returns (bool);
	function initialize(address _id, address _advocateId, address _listenerId, address _speakerId) external returns (bool);
	function determinePosition(address _sender, address _id) external view returns (uint256);
}
contract TokenERC20 {
	string public name;
	string public symbol;
	uint8 public decimals = 18;
	uint256 public totalSupply;
	mapping (address => uint256) public balanceOf;
	mapping (address => mapping (address => uint256)) public allowance;
	event Transfer(address indexed from, address indexed to, uint256 value);
	event Approval(address indexed _owner, address indexed _spender, uint256 _value);
	event Burn(address indexed from, uint256 value);
	constructor (uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
		totalSupply = initialSupply * 10 ** uint256(decimals);  
		balanceOf[msg.sender] = totalSupply;                
		name = tokenName;                                   
		symbol = tokenSymbol;                               
	}
	function _transfer(address _from, address _to, uint _value) internal {
		require(_to != address(0));
		require(balanceOf[_from] >= _value);
		require(balanceOf[_to] + _value > balanceOf[_to]);
		uint previousBalances = balanceOf[_from] + balanceOf[_to];
		balanceOf[_from] -= _value;
		balanceOf[_to] += _value;
		emit Transfer(_from, _to, _value);
		assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
	}
	function transfer(address _to, uint256 _value) public returns (bool success) {
		_transfer(msg.sender, _to, _value);
		return true;
	}
	function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
		require(_value <= allowance[_from][msg.sender]);     
		allowance[_from][msg.sender] -= _value;
		_transfer(_from, _to, _value);
		return true;
	}
	function approve(address _spender, uint256 _value) public returns (bool success) {
		allowance[msg.sender][_spender] = _value;
		emit Approval(msg.sender, _spender, _value);
		return true;
	}
	function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success) {
		tokenRecipient spender = tokenRecipient(_spender);
		if (approve(_spender, _value)) {
			spender.receiveApproval(msg.sender, _value, address(this), _extraData);
			return true;
		}
	}
	function burn(uint256 _value) public returns (bool success) {
		require(balanceOf[msg.sender] >= _value);   
		balanceOf[msg.sender] -= _value;            
		totalSupply -= _value;                      
		emit Burn(msg.sender, _value);
		return true;
	}
	function burnFrom(address _from, uint256 _value) public returns (bool success) {
		require(balanceOf[_from] >= _value);                
		require(_value <= allowance[_from][msg.sender]);    
		balanceOf[_from] -= _value;                         
		allowance[_from][msg.sender] -= _value;             
		totalSupply -= _value;                              
		emit Burn(_from, _value);
		return true;
	}
}
interface INameAccountRecovery {
	function isCompromised(address _id) external view returns (bool);
}
interface INameFactory {
	function nonces(address _nameId) external view returns (uint256);
	function incrementNonce(address _nameId) external returns (uint256);
	function ethAddressToNameId(address _ethAddress) external view returns (address);
	function setNameNewAddress(address _id, address _newAddress) external returns (bool);
	function nameIdToEthAddress(address _nameId) external view returns (address);
}
interface ITAOPool {
	function createPool(address _taoId, bool _ethosCapStatus, uint256 _ethosCapAmount) external returns (bool);
}
interface IAOSetting {
	function getSettingValuesByTAOName(address _taoId, string calldata _settingName) external view returns (uint256, bool, address, bytes32, string memory);
	function getSettingTypes() external view returns (uint8, uint8, uint8, uint8, uint8);
	function settingTypeLookup(uint256 _settingId) external view returns (uint8);
}
interface ITAOAncestry {
	function initialize(address _id, address _parentId, uint256 _childMinLogos) external returns (bool);
	function getAncestryById(address _id) external view returns (address, uint256, uint256);
	function addChild(address _taoId, address _childId) external returns (bool);
	function isChild(address _taoId, address _childId) external view returns (bool);
}
interface INameTAOLookup {
	function isExist(string calldata _name) external view returns (bool);
	function initialize(string calldata _name, address _nameTAOId, uint256 _typeId, string calldata _parentName, address _parentId, uint256 _parentTypeId) external returns (bool);
	function getById(address _id) external view returns (string memory, address, uint256, string memory, address, uint256);
	function getIdByName(string calldata _name) external view returns (address);
}
interface ITAOFactory {
	function nonces(address _taoId) external view returns (uint256);
	function incrementNonce(address _taoId) external returns (uint256);
}
contract TAO {
	using SafeMath for uint256;
	address public vaultAddress;
	string public name;				
	address public originId;		
	string public datHash;
	string public database;
	string public keyValue;
	bytes32 public contentId;
	uint8 public typeId;
	constructor (string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _vaultAddress
	) public {
		name = _name;
		originId = _originId;
		datHash = _datHash;
		database = _database;
		keyValue = _keyValue;
		contentId = _contentId;
		typeId = 0;
		vaultAddress = _vaultAddress;
	}
	modifier onlyVault {
		require (msg.sender == vaultAddress);
		_;
	}
	function () external payable {
	}
	function transferEth(address payable _recipient, uint256 _amount) public onlyVault returns (bool) {
		_recipient.transfer(_amount);
		return true;
	}
	function transferERC20(address _erc20TokenAddress, address _recipient, uint256 _amount) public onlyVault returns (bool) {
		TokenERC20 _erc20 = TokenERC20(_erc20TokenAddress);
		_erc20.transfer(_recipient, _amount);
		return true;
	}
}
contract Name is TAO {
	constructor (string memory _name, address _originId, string memory _datHash, string memory _database, string memory _keyValue, bytes32 _contentId, address _vaultAddress)
		TAO (_name, _originId, _datHash, _database, _keyValue, _contentId, _vaultAddress) public {
		typeId = 1;
	}
}
library AOLibrary {
	using SafeMath for uint256;
	uint256 constant private _MULTIPLIER_DIVISOR = 10 ** 6; 
	uint256 constant private _PERCENTAGE_DIVISOR = 10 ** 6; 
	function isTAO(address _taoId) public view returns (bool) {
		return (_taoId != address(0) && bytes(TAO(address(uint160(_taoId))).name()).length > 0 && TAO(address(uint160(_taoId))).originId() != address(0) && TAO(address(uint160(_taoId))).typeId() == 0);
	}
	function isName(address _nameId) public view returns (bool) {
		return (_nameId != address(0) && bytes(TAO(address(uint160(_nameId))).name()).length > 0 && Name(address(uint160(_nameId))).originId() != address(0) && Name(address(uint160(_nameId))).typeId() == 1);
	}
	function isValidERC20TokenAddress(address _tokenAddress) public view returns (bool) {
		if (_tokenAddress == address(0)) {
			return false;
		}
		TokenERC20 _erc20 = TokenERC20(_tokenAddress);
		return (_erc20.totalSupply() >= 0 && bytes(_erc20.name()).length > 0 && bytes(_erc20.symbol()).length > 0);
	}
	function isTheAO(address _sender, address _theAO, address _nameTAOPositionAddress) public view returns (bool) {
		return (_sender == _theAO ||
			(
				(isTAO(_theAO) || isName(_theAO)) &&
				_nameTAOPositionAddress != address(0) &&
				INameTAOPosition(_nameTAOPositionAddress).senderIsAdvocate(_sender, _theAO)
			)
		);
	}
	function PERCENTAGE_DIVISOR() public pure returns (uint256) {
		return _PERCENTAGE_DIVISOR;
	}
	function MULTIPLIER_DIVISOR() public pure returns (uint256) {
		return _MULTIPLIER_DIVISOR;
	}
	function deployTAO(string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _nameTAOVaultAddress
		) public returns (TAO _tao) {
		_tao = new TAO(_name, _originId, _datHash, _database, _keyValue, _contentId, _nameTAOVaultAddress);
	}
	function deployName(string memory _name,
		address _originId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _nameTAOVaultAddress
		) public returns (Name _myName) {
		_myName = new Name(_name, _originId, _datHash, _database, _keyValue, _contentId, _nameTAOVaultAddress);
	}
	function calculateWeightedMultiplier(uint256 _currentWeightedMultiplier, uint256 _currentPrimordialBalance, uint256 _additionalWeightedMultiplier, uint256 _additionalPrimordialAmount) public pure returns (uint256) {
		if (_currentWeightedMultiplier > 0) {
			uint256 _totalWeightedIons = (_currentWeightedMultiplier.mul(_currentPrimordialBalance)).add(_additionalWeightedMultiplier.mul(_additionalPrimordialAmount));
			uint256 _totalIons = _currentPrimordialBalance.add(_additionalPrimordialAmount);
			return _totalWeightedIons.div(_totalIons);
		} else {
			return _additionalWeightedMultiplier;
		}
	}
	function calculatePrimordialMultiplier(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		if (_purchaseAmount > 0 && _purchaseAmount <= _totalPrimordialMintable.sub(_totalPrimordialMinted)) {
			uint256 temp = _totalPrimordialMinted.add(_purchaseAmount.div(2));
			uint256 multiplier = (_MULTIPLIER_DIVISOR.sub(_MULTIPLIER_DIVISOR.mul(temp).div(_totalPrimordialMintable))).mul(_startingMultiplier.sub(_endingMultiplier));
			return multiplier.div(_MULTIPLIER_DIVISOR);
		} else {
			return 0;
		}
	}
	function calculateNetworkBonusPercentage(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		if (_purchaseAmount > 0 && _purchaseAmount <= _totalPrimordialMintable.sub(_totalPrimordialMinted)) {
			uint256 temp = _totalPrimordialMinted.add(_purchaseAmount.div(2));
			uint256 bonusPercentage = (_PERCENTAGE_DIVISOR.sub(_PERCENTAGE_DIVISOR.mul(temp).div(_totalPrimordialMintable))).mul(_startingMultiplier.sub(_endingMultiplier)).div(_PERCENTAGE_DIVISOR);
			return bonusPercentage;
		} else {
			return 0;
		}
	}
	function calculateNetworkBonusAmount(uint256 _purchaseAmount, uint256 _totalPrimordialMintable, uint256 _totalPrimordialMinted, uint256 _startingMultiplier, uint256 _endingMultiplier) public pure returns (uint256) {
		uint256 bonusPercentage = calculateNetworkBonusPercentage(_purchaseAmount, _totalPrimordialMintable, _totalPrimordialMinted, _startingMultiplier, _endingMultiplier);
		uint256 networkBonus = bonusPercentage.mul(_purchaseAmount).div(_PERCENTAGE_DIVISOR);
		return networkBonus;
	}
	function calculateMaximumBurnAmount(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _maximumMultiplier) public pure returns (uint256) {
		return (_maximumMultiplier.mul(_primordialBalance).sub(_primordialBalance.mul(_currentWeightedMultiplier))).div(_maximumMultiplier);
	}
	function calculateMultiplierAfterBurn(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _amountToBurn) public pure returns (uint256) {
		return _primordialBalance.mul(_currentWeightedMultiplier).div(_primordialBalance.sub(_amountToBurn));
	}
	function calculateMultiplierAfterConversion(uint256 _primordialBalance, uint256 _currentWeightedMultiplier, uint256 _amountToConvert) public pure returns (uint256) {
		return _primordialBalance.mul(_currentWeightedMultiplier).div(_primordialBalance.add(_amountToConvert));
	}
	function numDigits(uint256 number) public pure returns (uint8) {
		uint8 digits = 0;
		while(number != 0) {
			number = number.div(10);
			digits++;
		}
		return digits;
	}
}
contract TAOController is TheAO {
	address public nameFactoryAddress;
	address public nameAccountRecoveryAddress;
	INameFactory internal _nameFactory;
	INameTAOPosition internal _nameTAOPosition;
	INameAccountRecovery internal _nameAccountRecovery;
	constructor(address _nameFactoryAddress) public {
		setNameFactoryAddress(_nameFactoryAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier isTAO(address _taoId) {
		require (AOLibrary.isTAO(_taoId));
		_;
	}
	modifier isName(address _nameId) {
		require (AOLibrary.isName(_nameId));
		_;
	}
	modifier isNameOrTAO(address _id) {
		require (AOLibrary.isName(_id) || AOLibrary.isTAO(_id));
		_;
	}
	 modifier senderIsName() {
		require (_nameFactory.ethAddressToNameId(msg.sender) != address(0));
		_;
	 }
	modifier onlyAdvocate(address _id) {
		require (_nameTAOPosition.senderIsAdvocate(msg.sender, _id));
		_;
	}
	modifier senderNameNotCompromised() {
		require (!_nameAccountRecovery.isCompromised(_nameFactory.ethAddressToNameId(msg.sender)));
		_;
	}
	function transferOwnership(address _theAO) public onlyTheAO {
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public onlyTheAO {
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
	function setNameFactoryAddress(address _nameFactoryAddress) public onlyTheAO {
		require (_nameFactoryAddress != address(0));
		nameFactoryAddress = _nameFactoryAddress;
		_nameFactory = INameFactory(_nameFactoryAddress);
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
		_nameTAOPosition = INameTAOPosition(_nameTAOPositionAddress);
	}
	function setNameAccountRecoveryAddress(address _nameAccountRecoveryAddress) public onlyTheAO {
		require (_nameAccountRecoveryAddress != address(0));
		nameAccountRecoveryAddress = _nameAccountRecoveryAddress;
		_nameAccountRecovery = INameAccountRecovery(nameAccountRecoveryAddress);
	}
}
contract TAOCurrency is TheAO {
	using SafeMath for uint256;
	string public name;
	string public symbol;
	uint8 public decimals;
	uint256 public powerOfTen;
	uint256 public totalSupply;
	mapping (address => uint256) public balanceOf;
	event Transfer(address indexed from, address indexed to, uint256 value);
	event Burn(address indexed from, uint256 value);
	constructor (string memory _name, string memory _symbol, address _nameTAOPositionAddress) public {
		name = _name;		
		symbol = _symbol;	
		powerOfTen = 0;
		decimals = 0;
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier onlyTheAO {
		require (AOLibrary.isTheAO(msg.sender, theAO, nameTAOPositionAddress));
		_;
	}
	modifier isNameOrTAO(address _id) {
		require (AOLibrary.isName(_id) || AOLibrary.isTAO(_id));
		_;
	}
	function transferOwnership(address _theAO) public onlyTheAO {
		require (_theAO != address(0));
		theAO = _theAO;
	}
	function setWhitelist(address _account, bool _whitelist) public onlyTheAO {
		require (_account != address(0));
		whitelist[_account] = _whitelist;
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
	}
	function transferFrom(address _from, address _to, uint256 _value) public inWhitelist isNameOrTAO(_from) isNameOrTAO(_to) returns (bool) {
		_transfer(_from, _to, _value);
		return true;
	}
	function mint(address target, uint256 mintedAmount) public inWhitelist isNameOrTAO(target) returns (bool) {
		_mint(target, mintedAmount);
		return true;
	}
	function whitelistBurnFrom(address _from, uint256 _value) public inWhitelist isNameOrTAO(_from) returns (bool success) {
		require(balanceOf[_from] >= _value);                
		balanceOf[_from] = balanceOf[_from].sub(_value);    
		totalSupply = totalSupply.sub(_value);              
		emit Burn(_from, _value);
		return true;
	}
	function _transfer(address _from, address _to, uint256 _value) internal {
		require (_to != address(0));							
		require (balanceOf[_from] >= _value);					
		require (balanceOf[_to].add(_value) >= balanceOf[_to]); 
		uint256 previousBalances = balanceOf[_from].add(balanceOf[_to]);
		balanceOf[_from] = balanceOf[_from].sub(_value);        
		balanceOf[_to] = balanceOf[_to].add(_value);            
		emit Transfer(_from, _to, _value);
		assert(balanceOf[_from].add(balanceOf[_to]) == previousBalances);
	}
	function _mint(address target, uint256 mintedAmount) internal {
		balanceOf[target] = balanceOf[target].add(mintedAmount);
		totalSupply = totalSupply.add(mintedAmount);
		emit Transfer(address(0), address(this), mintedAmount);
		emit Transfer(address(this), target, mintedAmount);
	}
}
contract Logos is TAOCurrency {
	address public nameFactoryAddress;
	address public nameAccountRecoveryAddress;
	INameFactory internal _nameFactory;
	INameTAOPosition internal _nameTAOPosition;
	INameAccountRecovery internal _nameAccountRecovery;
	mapping (address => uint256) public positionFromOthers;
	mapping (address => mapping(address => uint256)) public positionOnOthers;
	mapping (address => uint256) public totalPositionOnOthers;
	mapping (address => mapping(address => uint256)) public advocatedTAOLogos;
	mapping (address => uint256) public totalAdvocatedTAOLogos;
	event PositionFrom(address indexed from, address indexed to, uint256 value);
	event UnpositionFrom(address indexed from, address indexed to, uint256 value);
	event AddAdvocatedTAOLogos(address indexed nameId, address indexed taoId, uint256 amount);
	event TransferAdvocatedTAOLogos(address indexed fromNameId, address indexed toNameId, address indexed taoId, uint256 amount);
	constructor(string memory _name, string memory _symbol, address _nameFactoryAddress, address _nameTAOPositionAddress)
		TAOCurrency(_name, _symbol, _nameTAOPositionAddress) public {
		setNameFactoryAddress(_nameFactoryAddress);
		setNameTAOPositionAddress(_nameTAOPositionAddress);
	}
	modifier isTAO(address _taoId) {
		require (AOLibrary.isTAO(_taoId));
		_;
	}
	modifier isName(address _nameId) {
		require (AOLibrary.isName(_nameId));
		_;
	}
	modifier onlyAdvocate(address _id) {
		require (_nameTAOPosition.senderIsAdvocate(msg.sender, _id));
		_;
	}
	modifier nameNotCompromised(address _id) {
		require (!_nameAccountRecovery.isCompromised(_id));
		_;
	}
	modifier senderNameNotCompromised() {
		require (!_nameAccountRecovery.isCompromised(_nameFactory.ethAddressToNameId(msg.sender)));
		_;
	}
	function setNameFactoryAddress(address _nameFactoryAddress) public onlyTheAO {
		require (_nameFactoryAddress != address(0));
		nameFactoryAddress = _nameFactoryAddress;
		_nameFactory = INameFactory(_nameFactoryAddress);
	}
	function setNameTAOPositionAddress(address _nameTAOPositionAddress) public onlyTheAO {
		require (_nameTAOPositionAddress != address(0));
		nameTAOPositionAddress = _nameTAOPositionAddress;
		_nameTAOPosition = INameTAOPosition(_nameTAOPositionAddress);
	}
	function setNameAccountRecoveryAddress(address _nameAccountRecoveryAddress) public onlyTheAO {
		require (_nameAccountRecoveryAddress != address(0));
		nameAccountRecoveryAddress = _nameAccountRecoveryAddress;
		_nameAccountRecovery = INameAccountRecovery(nameAccountRecoveryAddress);
	}
	function sumBalanceOf(address _target) public isName(_target) view returns (uint256) {
		return balanceOf[_target].add(positionFromOthers[_target]).add(totalAdvocatedTAOLogos[_target]);
	}
	function availableToPositionAmount(address _sender) public isName(_sender) view returns (uint256) {
		return balanceOf[_sender].sub(totalPositionOnOthers[_sender]);
	}
	function positionFrom(address _from, address _to, uint256 _value) public isName(_from) isName(_to) nameNotCompromised(_from) nameNotCompromised(_to) onlyAdvocate(_from) senderNameNotCompromised returns (bool) {
		require (_from != _to);	
		require (availableToPositionAmount(_from) >= _value); 
		require (positionFromOthers[_to].add(_value) >= positionFromOthers[_to]); 
		positionOnOthers[_from][_to] = positionOnOthers[_from][_to].add(_value);
		totalPositionOnOthers[_from] = totalPositionOnOthers[_from].add(_value);
		positionFromOthers[_to] = positionFromOthers[_to].add(_value);
		emit PositionFrom(_from, _to, _value);
		return true;
	}
	function unpositionFrom(address _from, address _to, uint256 _value) public isName(_from) isName(_to) nameNotCompromised(_from) nameNotCompromised(_to) onlyAdvocate(_from) senderNameNotCompromised returns (bool) {
		require (_from != _to);	
		require (positionOnOthers[_from][_to] >= _value);
		positionOnOthers[_from][_to] = positionOnOthers[_from][_to].sub(_value);
		totalPositionOnOthers[_from] = totalPositionOnOthers[_from].sub(_value);
		positionFromOthers[_to] = positionFromOthers[_to].sub(_value);
		emit UnpositionFrom(_from, _to, _value);
		return true;
	}
	function addAdvocatedTAOLogos(address _taoId, uint256 _amount) public inWhitelist isTAO(_taoId) returns (bool) {
		require (_amount > 0);
		address _nameId = _nameTAOPosition.getAdvocate(_taoId);
		advocatedTAOLogos[_nameId][_taoId] = advocatedTAOLogos[_nameId][_taoId].add(_amount);
		totalAdvocatedTAOLogos[_nameId] = totalAdvocatedTAOLogos[_nameId].add(_amount);
		emit AddAdvocatedTAOLogos(_nameId, _taoId, _amount);
		return true;
	}
	function transferAdvocatedTAOLogos(address _fromNameId, address _taoId) public inWhitelist isName(_fromNameId) isTAO(_taoId) returns (bool) {
		address _toNameId = _nameTAOPosition.getAdvocate(_taoId);
		require (_fromNameId != _toNameId);
		require (totalAdvocatedTAOLogos[_fromNameId] >= advocatedTAOLogos[_fromNameId][_taoId]);
		uint256 _amount = advocatedTAOLogos[_fromNameId][_taoId];
		advocatedTAOLogos[_fromNameId][_taoId] = 0;
		totalAdvocatedTAOLogos[_fromNameId] = totalAdvocatedTAOLogos[_fromNameId].sub(_amount);
		advocatedTAOLogos[_toNameId][_taoId] = advocatedTAOLogos[_toNameId][_taoId].add(_amount);
		totalAdvocatedTAOLogos[_toNameId] = totalAdvocatedTAOLogos[_toNameId].add(_amount);
		emit TransferAdvocatedTAOLogos(_fromNameId, _toNameId, _taoId, _amount);
		return true;
	}
}
contract TAOFactory is TAOController, ITAOFactory {
	using SafeMath for uint256;
	address[] internal taos;
	address public nameTAOLookupAddress;
	address public aoSettingAddress;
	address public logosAddress;
	address public nameTAOVaultAddress;
	address public taoAncestryAddress;
	address public settingTAOId;
	address public taoPoolAddress;
	INameTAOLookup internal _nameTAOLookup;
	IAOSetting internal _aoSetting;
	Logos internal _logos;
	ITAOAncestry internal _taoAncestry;
	ITAOPool internal _taoPool;
	mapping (address => uint256) internal _nonces;
	event CreateTAO(address indexed advocateId, address taoId, uint256 index, string name, address parent, uint8 parentTypeId);
	constructor(address _nameFactoryAddress)
		TAOController(_nameFactoryAddress) public {}
	modifier canUpdateNonce {
		require (msg.sender == nameTAOPositionAddress || msg.sender == taoAncestryAddress || msg.sender == taoPoolAddress);
		_;
	}
	function setNameTAOLookupAddress(address _nameTAOLookupAddress) public onlyTheAO {
		require (_nameTAOLookupAddress != address(0));
		nameTAOLookupAddress = _nameTAOLookupAddress;
		_nameTAOLookup = INameTAOLookup(_nameTAOLookupAddress);
	}
	function setAOSettingAddress(address _aoSettingAddress) public onlyTheAO {
		require (_aoSettingAddress != address(0));
		aoSettingAddress = _aoSettingAddress;
		_aoSetting = IAOSetting(_aoSettingAddress);
	}
	function setLogosAddress(address _logosAddress) public onlyTheAO {
		require (_logosAddress != address(0));
		logosAddress = _logosAddress;
		_logos = Logos(_logosAddress);
	}
	function setNameTAOVaultAddress(address _nameTAOVaultAddress) public onlyTheAO {
		require (_nameTAOVaultAddress != address(0));
		nameTAOVaultAddress = _nameTAOVaultAddress;
	}
	function setTAOAncestryAddress(address _taoAncestryAddress) public onlyTheAO {
		require (_taoAncestryAddress != address(0));
		taoAncestryAddress = _taoAncestryAddress;
		_taoAncestry = ITAOAncestry(taoAncestryAddress);
	}
	function setSettingTAOId(address _settingTAOId) public onlyTheAO isTAO(_settingTAOId) {
		settingTAOId = _settingTAOId;
	}
	function setTAOPoolAddress(address _taoPoolAddress) public onlyTheAO {
		require (_taoPoolAddress != address(0));
		taoPoolAddress = _taoPoolAddress;
		_taoPool = ITAOPool(taoPoolAddress);
	}
	function nonces(address _taoId) external view returns (uint256) {
		return _nonces[_taoId];
	}
	function incrementNonce(address _taoId) external canUpdateNonce returns (uint256) {
		require (_nonces[_taoId] > 0);
		_nonces[_taoId]++;
		return _nonces[_taoId];
	}
	function createTAO(
		string memory _name,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _parentId,
		uint256 _childMinLogos,
		bool _ethosCapStatus,
		uint256 _ethosCapAmount
	) public senderIsName senderNameNotCompromised isNameOrTAO(_parentId) {
		require (bytes(_name).length > 0);
		require (!_nameTAOLookup.isExist(_name));
		uint256 _nameSumLogos = _logos.sumBalanceOf(_nameFactory.ethAddressToNameId(msg.sender));
		if (AOLibrary.isTAO(_parentId)) {
			(, uint256 _parentCreateChildTAOMinLogos,) = _taoAncestry.getAncestryById(_parentId);
			require (_nameSumLogos >= _parentCreateChildTAOMinLogos);
		} else {
			require (_nameSumLogos >= _getCreateChildTAOMinLogos());
		}
		require (_createTAO(_name, _nameFactory.ethAddressToNameId(msg.sender), _datHash, _database, _keyValue, _contentId, _parentId, _childMinLogos, _ethosCapStatus, _ethosCapAmount));
	}
	function getTAO(address _taoId) public view returns (string memory, address, string memory, string memory, string memory, string memory, bytes32, uint8) {
		TAO _tao = TAO(address(uint160(_taoId)));
		return (
			_tao.name(),
			_tao.originId(),
			Name(address(uint160(_tao.originId()))).name(),
			_tao.datHash(),
			_tao.database(),
			_tao.keyValue(),
			_tao.contentId(),
			_tao.typeId()
		);
	}
	function getTotalTAOsCount() public view returns (uint256) {
		return taos.length;
	}
	function getTAOIds(uint256 _from, uint256 _to) public view returns (address[] memory) {
		require (_from >= 0 && _to >= _from);
		require (taos.length > 0);
		address[] memory _taos = new address[](_to.sub(_from).add(1));
		if (_to > taos.length.sub(1)) {
			_to = taos.length.sub(1);
		}
		for (uint256 i = _from; i <= _to; i++) {
			_taos[i.sub(_from)] = taos[i];
		}
		return _taos;
	}
	function validateTAOSignature(
		string memory _data,
		uint256 _nonce,
		address _validateAddress,
		string memory _name,
		uint8 _signatureV,
		bytes32 _signatureR,
		bytes32 _signatureS
	) public isTAO(_getTAOIdByName(_name)) view returns (bool, string memory, uint256) {
		address _signatureAddress = _getValidateSignatureAddress(_data, _nonce, _signatureV, _signatureR, _signatureS);
		if (_isTAOSignatureAddressValid(_validateAddress, _signatureAddress, _getTAOIdByName(_name), _nonce)) {
			return (true, Name(address(uint160(_nameFactory.ethAddressToNameId(_signatureAddress)))).name(), _nameTAOPosition.determinePosition(_signatureAddress, _getTAOIdByName(_name)));
		} else {
			return (false, "", 0);
		}
	}
	function _createTAO(
		string memory _name,
		address _nameId,
		string memory _datHash,
		string memory _database,
		string memory _keyValue,
		bytes32 _contentId,
		address _parentId,
		uint256 _childMinLogos,
		bool _ethosCapStatus,
		uint256 _ethosCapAmount
	) internal returns (bool) {
		address taoId = address(AOLibrary.deployTAO(_name, _nameId, _datHash, _database, _keyValue, _contentId, nameTAOVaultAddress));
		_nonces[taoId]++;
		require (_nameTAOLookup.initialize(_name, taoId, 0, TAO(address(uint160(_parentId))).name(), _parentId, uint256(TAO(address(uint160(_parentId))).typeId())));
		require (_nameTAOPosition.initialize(taoId, _nameId, _nameId, _nameId));
		require (_taoAncestry.initialize(taoId, _parentId, _childMinLogos));
		require (_taoPool.createPool(taoId, _ethosCapStatus, _ethosCapAmount));
		taos.push(taoId);
		emit CreateTAO(_nameId, taoId, taos.length.sub(1), _name, _parentId, TAO(address(uint160(_parentId))).typeId());
		if (AOLibrary.isTAO(_parentId)) {
			require (_taoAncestry.addChild(_parentId, taoId));
		}
		return true;
	}
	function _isTAOSignatureAddressValid(
		address _validateAddress,
		address _signatureAddress,
		address _taoId,
		uint256 _nonce
	) internal view returns (bool) {
		if (_validateAddress != address(0)) {
			return (_nonce == _nonces[_taoId].add(1) &&
				_signatureAddress == _validateAddress &&
				_nameTAOPosition.senderIsPosition(_validateAddress, _taoId)
			);
		} else {
			return (
				_nonce == _nonces[_taoId].add(1) &&
				_nameTAOPosition.senderIsPosition(_signatureAddress, _taoId)
			);
		}
	}
	function _getTAOIdByName(string memory _name) internal view returns (address) {
		return _nameTAOLookup.getIdByName(_name);
	}
	function _getCreateChildTAOMinLogos() internal view returns (uint256) {
		(uint256 createChildTAOMinLogos,,,,) = _aoSetting.getSettingValuesByTAOName(settingTAOId, 'createChildTAOMinLogos');
		return createChildTAOMinLogos;
	}
	function _getValidateSignatureAddress(string memory _data, uint256 _nonce, uint8 _v, bytes32 _r, bytes32 _s) internal view returns (address) {
		bytes32 _hash = keccak256(abi.encodePacked(address(this), _data, _nonce));
		return ecrecover(_hash, _v, _r, _s);
	}
}
```

## RQ1_da205520b7b6

SHA-256 `06177a909a666c4bfe01659452e96f5de04663fab214825282c09d3e965629e4`

```solidity
pragma solidity ^0.4.24;
contract EDProxy {
    function EDProxy() public {
    }
    function dtrade(address _callee, uint8 v1, uint8 v2, uint256[] uints,address[] addresses,bytes32[] b) public {
        if (_callee.delegatecall(bytes4(keccak256("trade(address,uint256,address,uint256,uint256,uint256,address,uint8,bytes32,bytes32,uint256)")),
          addresses[0],
          uints[0],
          addresses[2],
          uints[2],
          uints[4],
          uints[6],
          addresses[4],
          v1,
          b[0],
          b[2],
          uints[8]
          )) {
        (_callee.delegatecall(bytes4(keccak256("trade(address,uint256,address,uint256,uint256,uint256,address,uint8,bytes32,bytes32,uint256)")),
           addresses[1],
           uints[1],
           addresses[3],
           uints[3],
           uints[5],
           uints[7],
           addresses[5],
           v2,
           b[1],
           b[3],
           uints[9]
           ));
          }
    }
     function testcall(address _callee)  public {
        bytes32[] memory b = new bytes32[](4);
        address[] memory addrs = new address[](6);
        uint256[] memory ints = new uint256[](12);
        uint8 v1;
        uint8 v2;
        bytes32 somebytes;
        ints[0]=1;
        ints[1]=2;
        ints[2]=3;
        ints[3]=4;
        ints[4]=5;
        ints[5]=6;
        ints[6]=7;
        ints[7]=8;
        ints[8]=9;
        ints[9]=10;
        v1=11;
        v2=12;
        b[0]=somebytes;
        b[1]=somebytes;
        b[2]=somebytes;
        b[3]=somebytes;
        addrs[0]=0xdc04977a2078c8ffdf086d618d1f961b6c54111;
        addrs[1]=0xdc04977a2078c8ffdf086d618d1f961b6c54222;
        addrs[2]=0xdc04977a2078c8ffdf086d618d1f961b6c54333;
        addrs[3]=0xdc04977a2078c8ffdf086d618d1f961b6c54444;
        addrs[4]=0xdc04977a2078c8ffdf086d618d1f961b6c54555;
        addrs[5]=0xdc04977a2078c8ffdf086d618d1f961b6c54666;
        dtrade(_callee, v1, v2, ints, addrs,b);
    }
}
```

## RQ1_ae3727e56084

SHA-256 `e1af2d52fa68604d1b880ac2493bbd90468a1c9dc6c13f0a8bc48161aaf398ad`

```solidity
pragma solidity ^0.4.18;
contract Dividend {
    struct Record {
        uint balance;
        uint shares;
        uint index;
    }
    mapping (address => Record) public records;
    address[] public investors;
    address public funder;
    uint public startTime;
    uint public totalShares;
    uint public lastInvestmentTime;
    event Invested(uint indexed timestamp, address indexed from, uint amount, uint shares);
    event Withdrawn(uint indexed timestamp, address indexed from, uint amount);
    function Dividend() public payable {
        records[msg.sender] = Record(msg.value,
            totalShares = allocateShares(msg.value, 0),
            investors.push(funder = msg.sender));
        Invested(startTime = lastInvestmentTime = now, msg.sender, msg.value, totalShares);
    }
    function () public payable {
        invest();
    }
    function investorCount() public view returns (uint) {
      return investors.length;
    }
    function invest() public payable returns (uint) {
        uint value = msg.value;
        uint shares = allocateShares(value, (now - startTime) / 1 hours);
        if (shares > 0) {
            for (uint i = investors.length; i > 0; i--) {
                Record storage rec = records[investors[i - 1]];
                rec.balance += value * rec.shares / totalShares;
            }
            address investor = msg.sender;
            rec = records[investor];
            if (rec.index > 0) {
                rec.shares += shares;
            } else {
                rec.shares = shares;
                rec.index = investors.push(investor);
            }
            totalShares += shares;
            Invested(lastInvestmentTime = now, investor, value, shares);
        }
        return shares;
    }
    function withdraw() public returns (uint) {
        Record storage rec = records[msg.sender];
        uint balance = rec.balance;
        if (balance > 0) {
            rec.balance = 0;
            msg.sender.transfer(balance);
            Withdrawn(now, msg.sender, balance);
        }
        if (now - lastInvestmentTime > 4 weeks) {
            selfdestruct(funder);
        }
        return balance;
    }
    function allocateShares(uint weis, uint bonus) public pure returns (uint) {
        return weis * (1000 + bonus) / 1 ether;
    }
}
```

## RQ1_5e3e429093e1

SHA-256 `2804494d19c3de0b9bf5d4f8d2eb0311f4181842357e7deb6cda6cb31fd387b7`

```solidity
pragma solidity ^0.5.1;
library IterableMapping {
  struct itmap
  {
    mapping(address => IndexValue) data;
    KeyFlag[] keys;
    uint size;
  }
  struct IndexValue { uint keyIndex; uint value; }
  struct KeyFlag { address key; bool deleted; }
  function insert(itmap storage self, address key, uint value) public returns (bool replaced)
  {
    uint keyIndex = self.data[key].keyIndex;
    self.data[key].value = value;
    if (keyIndex > 0)
      return true;
    else
    {
      keyIndex = self.keys.length++;
      self.data[key].keyIndex = keyIndex + 1;
      self.keys[keyIndex].key = key;
      self.size++;
      return false;
    }
  }
  function remove(itmap storage self, address key) public returns (bool success)
  {
    uint keyIndex = self.data[key].keyIndex;
    if (keyIndex == 0)
      return false;
    delete self.data[key];
    self.keys[keyIndex - 1].deleted = true;
    self.size --;
  }
  function contains(itmap storage self, address key) public view returns (bool)
  {
    return self.data[key].keyIndex > 0;
  }
  function iterate_start(itmap storage self) public view returns (uint keyIndex)
  {
    return iterate_next(self, uint(-1));
  }
  function iterate_valid(itmap storage self, uint keyIndex) public view returns (bool)
  {
    return keyIndex < self.keys.length;
  }
  function iterate_next(itmap storage self, uint keyIndex) public view returns (uint r_keyIndex)
  {
    keyIndex++;
    while (keyIndex < self.keys.length && self.keys[keyIndex].deleted)
      keyIndex++;
    return keyIndex;
  }
  function iterate_get(itmap storage self, uint keyIndex) public view returns (address key, uint value)
  {
    key = self.keys[keyIndex].key;
    value = self.data[key].value;
  }
  function iterate_getValue(itmap storage self, address key) public view returns (uint value) {
      return self.data[key].value;
  }
}
library SafeMath {
  function mul(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    if (_a == 0) {
      return 0;
    }
    c = _a * _b;
    assert(c / _a == _b);
    return c;
  }
  function div(uint256 _a, uint256 _b) internal pure returns (uint256) {
    assert(_b > 0); 
    uint256 c = _a / _b;
    assert(_a == _b * c + _a % _b); 
    return _a / _b;
  }
  function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
    assert(_b <= _a);
    return _a - _b;
  }
  function add(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    c = _a + _b;
    assert(c >= _a);
    return c;
  }
}
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address _who) public view returns (uint256);
  function transfer(address _to, uint256 _value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;
  IterableMapping.itmap balances;
  uint256 internal totalSupply_;
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_value <= IterableMapping.iterate_getValue(balances, msg.sender));
    require(_to != address(0));
    IterableMapping.insert(balances, msg.sender, IterableMapping.iterate_getValue(balances, msg.sender).sub(_value));
    IterableMapping.insert(balances, _to, IterableMapping.iterate_getValue(balances, _to).add(_value));
    emit Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public view returns (uint256) {
      return IterableMapping.iterate_getValue(balances, _owner);
  }
}
contract ERC20 is ERC20Basic {
  function allowance(address _owner, address _spender)
    public view returns (uint256);
  function transferFrom(address _from, address _to, uint256 _value)
    public returns (bool);
  function approve(address _spender, uint256 _value) public returns (bool);
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    public
    returns (bool)
  {
    require(_value <= IterableMapping.iterate_getValue(balances, _from));
    require(_value <= allowed[_from][msg.sender]);
    require(_to != address(0));
    IterableMapping.insert(balances, _from, IterableMapping.iterate_getValue(balances, _from).sub(_value));
    IterableMapping.insert(balances, _to, IterableMapping.iterate_getValue(balances, _to).add(_value));
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    emit Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(
    address _owner,
    address _spender
   )
    public
    view
    returns (uint256)
  {
    return allowed[_owner][_spender];
  }
  function increaseApproval(
    address _spender,
    uint256 _addedValue
  )
    public
    returns (bool)
  {
    allowed[msg.sender][_spender] = (
      allowed[msg.sender][_spender].add(_addedValue));
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval(
    address _spender,
    uint256 _subtractedValue
  )
    public
    returns (bool)
  {
    uint256 oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue >= oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
}
contract IBNEST is StandardToken {
    string public name = "NEST";
    string public symbol = "NEST";
    uint8 public decimals = 18;
    uint256 public INITIAL_SUPPLY = 10000000000 ether;
    constructor () public {
    	totalSupply_ = INITIAL_SUPPLY;
    	IterableMapping.insert(balances, tx.origin, INITIAL_SUPPLY);
    }
    function balancesStart() public view returns(uint256) {
        return IterableMapping.iterate_start(balances);
    }
    function balancesGetBool(uint256 num) public view returns(bool){
        return IterableMapping.iterate_valid(balances, num);
    }
    function balancesGetNext(uint256 num) public view returns(uint256) {
        return IterableMapping.iterate_next(balances, num);
    }
    function balancesGetValue(uint256 num) public view returns(address, uint256) {
        address key;                           
        uint256 value;                         
        (key, value) = IterableMapping.iterate_get(balances, num);
        return (key, value);
    }
}
```

## RQ1_8400be2dc985

SHA-256 `9ba625a5e0eae1b0820594c9a4497d398e9155efcd92caae45f42fa8a5b44a28`

```solidity
pragma solidity ^0.4.24;
contract GodMode {
    bool public isPaused;
    address public god;
    modifier onlyGod()
    {
        require(god == msg.sender);
        _;
    }
    modifier notPaused()
    {
        require(!isPaused);
        _;
    }
    event GodPaused();
    event GodUnpaused();
    constructor() public
    {
        god = msg.sender;
    }
    function godChangeGod(address _newGod) public onlyGod
    {
        god = _newGod;
    }
    function godPause() public onlyGod
    {
        isPaused = true;
        emit GodPaused();
    }
    function godUnpause() public onlyGod
    {
        isPaused = false;
        emit GodUnpaused();
    }
}
pragma solidity ^0.4.24;
contract KingOfEthAuctionsAbstractInterface {
    function existingAuction(uint _x, uint _y) public view returns(bool);
}
pragma solidity ^0.4.24;
contract KingOfEthBlindAuctionsReferencer is GodMode {
    address public blindAuctionsContract;
    modifier onlyBlindAuctionsContract()
    {
        require(blindAuctionsContract == msg.sender);
        _;
    }
    function godSetBlindAuctionsContract(address _blindAuctionsContract)
        public
        onlyGod
    {
        blindAuctionsContract = _blindAuctionsContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthOpenAuctionsReferencer is GodMode {
    address public openAuctionsContract;
    modifier onlyOpenAuctionsContract()
    {
        require(openAuctionsContract == msg.sender);
        _;
    }
    function godSetOpenAuctionsContract(address _openAuctionsContract)
        public
        onlyGod
    {
        openAuctionsContract = _openAuctionsContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthAuctionsReferencer is
      KingOfEthBlindAuctionsReferencer
    , KingOfEthOpenAuctionsReferencer
{
    modifier onlyAuctionsContract()
    {
        require(blindAuctionsContract == msg.sender
             || openAuctionsContract == msg.sender);
        _;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthAbstractInterface {
    address public king;
    address public wayfarer;
    function payTaxes() public payable;
}
pragma solidity ^0.4.24;
contract KingOfEthReferencer is GodMode {
    address public kingOfEthContract;
    modifier onlyKingOfEthContract()
    {
        require(kingOfEthContract == msg.sender);
        _;
    }
    function godSetKingOfEthContract(address _kingOfEthContract)
        public
        onlyGod
    {
        kingOfEthContract = _kingOfEthContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthBoard is
      GodMode
    , KingOfEthAuctionsReferencer
    , KingOfEthReferencer
{
    uint public boundX1 = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffef;
    uint public boundY1 = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffef;
    uint public boundX2 = 0x800000000000000000000000000000000000000000000000000000000000000f;
    uint public boundY2 = 0x800000000000000000000000000000000000000000000000000000000000000f;
    uint public constant auctionsAvailableDivisor = 10;
    uint public constant kingTimeBetweenIncrease = 2 weeks;
    uint public constant wayfarerTimeBetweenIncrease = 3 weeks;
    uint public constant plebTimeBetweenIncrease = 4 weeks;
    uint public lastIncreaseTime;
    uint8 public nextIncreaseDirection;
    uint public auctionsRemaining;
    constructor() public
    {
        isPaused = true;
        setAuctionsAvailableForBounds();
    }
    event BoardSizeIncreased(
          address initiator
        , uint newBoundX1
        , uint newBoundY1
        , uint newBoundX2
        , uint newBoundY2
        , uint lastIncreaseTime
        , uint nextIncreaseDirection
        , uint auctionsRemaining
    );
    modifier onlyKing()
    {
        require(KingOfEthAbstractInterface(kingOfEthContract).king() == msg.sender);
        _;
    }
    modifier onlyWayfarer()
    {
        require(KingOfEthAbstractInterface(kingOfEthContract).wayfarer() == msg.sender);
        _;
    }
    function setAuctionsAvailableForBounds() private
    {
        uint boundDiffX = boundX2 - boundX1;
        uint boundDiffY = boundY2 - boundY1;
        auctionsRemaining = boundDiffX * boundDiffY / 2 / auctionsAvailableDivisor;
    }
    function increaseBoard() private
    {
        uint _increaseLength;
        if(0 == nextIncreaseDirection)
        {
            _increaseLength = boundX2 - boundX1;
            uint _updatedX2 = boundX2 + _increaseLength;
            if(_updatedX2 <= boundX2 || _updatedX2 <= _increaseLength)
            {
                boundX2 = ~uint(0);
            }
            else
            {
                boundX2 = _updatedX2;
            }
        }
        else if(1 == nextIncreaseDirection)
        {
            _increaseLength = boundY2 - boundY1;
            uint _updatedY2 = boundY2 + _increaseLength;
            if(_updatedY2 <= boundY2 || _updatedY2 <= _increaseLength)
            {
                boundY2 = ~uint(0);
            }
            else
            {
                boundY2 = _updatedY2;
            }
        }
        else if(2 == nextIncreaseDirection)
        {
            _increaseLength = boundX2 - boundX1;
            if(boundX1 <= _increaseLength)
            {
                boundX1 = 0;
            }
            else
            {
                boundX1 -= _increaseLength;
            }
        }
        else if(3 == nextIncreaseDirection)
        {
            _increaseLength = boundY2 - boundY1;
            if(boundY1 <= _increaseLength)
            {
                boundY1 = 0;
            }
            else
            {
                boundY1 -= _increaseLength;
            }
        }
        lastIncreaseTime = now;
        nextIncreaseDirection = (nextIncreaseDirection + 1) % 4;
        setAuctionsAvailableForBounds();
        emit BoardSizeIncreased(
              msg.sender
            , boundX1
            , boundY1
            , boundX2
            , boundY2
            , now
            , nextIncreaseDirection
            , auctionsRemaining
        );
    }
    function godStartGame() public onlyGod
    {
        lastIncreaseTime = now;
        godUnpause();
    }
    function auctionsDecrementAuctionsRemaining()
        public
        onlyAuctionsContract
    {
        auctionsRemaining -= 1;
    }
    function auctionsIncrementAuctionsRemaining()
        public
        onlyAuctionsContract
    {
        auctionsRemaining += 1;
    }
    function kingIncreaseBoard()
        public
        onlyKing
    {
        require(lastIncreaseTime + kingTimeBetweenIncrease < now);
        increaseBoard();
    }
    function wayfarerIncreaseBoard()
        public
        onlyWayfarer
    {
        require(lastIncreaseTime + wayfarerTimeBetweenIncrease < now);
        increaseBoard();
    }
    function plebIncreaseBoard() public
    {
        require(lastIncreaseTime + plebTimeBetweenIncrease < now);
        increaseBoard();
    }
}
pragma solidity ^0.4.24;
contract KingOfEthBoardReferencer is GodMode {
    address public boardContract;
    modifier onlyBoardContract()
    {
        require(boardContract == msg.sender);
        _;
    }
    function godSetBoardContract(address _boardContract)
        public
        onlyGod
    {
        boardContract = _boardContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthHousesAbstractInterface {
    function ownerOf(uint _x, uint _y) public view returns(address);
    function level(uint _x, uint _y) public view returns(uint8);
    function auctionsSetOwner(uint _x, uint _y, address _owner) public;
    function houseRealtyTransferOwnership(
          uint _x
        , uint _y
        , address _from
        , address _to
    ) public;
}
pragma solidity ^0.4.24;
contract KingOfEthHousesReferencer is GodMode {
    address public housesContract;
    modifier onlyHousesContract()
    {
        require(housesContract == msg.sender);
        _;
    }
    function godSetHousesContract(address _housesContract)
        public
        onlyGod
    {
        housesContract = _housesContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthHouseRealty is
      GodMode
    , KingOfEthHousesReferencer
    , KingOfEthReferencer
{
    uint public constant taxDivisor = 25;
    mapping (uint => mapping (uint => uint)) housePrices;
    event HouseForSale(
          uint x
        , uint y
        , address owner
        , uint amount
    );
    event HousePriceChanged(uint x, uint y, uint amount);
    event HouseSold(
          uint x
        , uint y
        , address from
        , address to
        , uint amount
        , uint8 level
    );
    event HouseSaleCancelled(
          uint x
        , uint y
        , address owner
    );
    modifier onlyHouseOwner(uint _x, uint _y)
    {
        require(KingOfEthHousesAbstractInterface(housesContract).ownerOf(_x, _y) == msg.sender);
        _;
    }
    modifier noExistingHouseSale(uint _x, uint _y)
    {
        require(0 == housePrices[_x][_y]);
        _;
    }
    modifier existingHouseSale(uint _x, uint _y)
    {
        require(0 != housePrices[_x][_y]);
        _;
    }
    constructor(address _kingOfEthContract) public
    {
        kingOfEthContract = _kingOfEthContract;
    }
    function housesCancelHouseSale(uint _x, uint _y)
        public
        onlyHousesContract
    {
        if(0 != housePrices[_x][_y])
        {
            housePrices[_x][_y] = 0;
            emit HouseSaleCancelled(_x, _y, msg.sender);
        }
    }
    function startHouseSale(uint _x, uint _y, uint _askingPrice)
        public
        notPaused
        onlyHouseOwner(_x, _y)
        noExistingHouseSale(_x, _y)
    {
        require(0 != _askingPrice);
        housePrices[_x][_y] = _askingPrice;
        emit HouseForSale(_x, _y, msg.sender, _askingPrice);
    }
    function changeHousePrice(uint _x, uint _y, uint _askingPrice)
        public
        notPaused
        onlyHouseOwner(_x, _y)
        existingHouseSale(_x, _y)
    {
        require(0 != _askingPrice);
        housePrices[_x][_y] = _askingPrice;
        emit HousePriceChanged(_x, _y, _askingPrice);
    }
    function purchaseHouse(uint _x, uint _y)
        public
        payable
        notPaused
        existingHouseSale(_x, _y)
    {
        require(housePrices[_x][_y] == msg.value);
        housePrices[_x][_y] = 0;
        uint taxCut = msg.value / taxDivisor;
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(taxCut)();
        KingOfEthHousesAbstractInterface _housesContract = KingOfEthHousesAbstractInterface(housesContract);
        address _oldOwner = _housesContract.ownerOf(_x, _y);
        _housesContract.houseRealtyTransferOwnership(
              _x
            , _y
            , _oldOwner
            , msg.sender
        );
        _oldOwner.transfer(msg.value - taxCut);
        emit HouseSold(
              _x
            , _y
            , _oldOwner
            , msg.sender
            , msg.value
            , _housesContract.level(_x, _y)
        );
    }
    function cancelHouseSale(uint _x, uint _y)
        public
        notPaused
        onlyHouseOwner(_x, _y)
        existingHouseSale(_x, _y)
    {
        housePrices[_x][_y] = 0;
        emit HouseSaleCancelled(_x, _y, msg.sender);
    }
}
pragma solidity ^0.4.24;
contract KingOfEthHouseRealtyReferencer is GodMode {
    address public houseRealtyContract;
    modifier onlyHouseRealtyContract()
    {
        require(houseRealtyContract == msg.sender);
        _;
    }
    function godSetHouseRealtyContract(address _houseRealtyContract)
        public
        onlyGod
    {
        houseRealtyContract = _houseRealtyContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthRoadsAbstractInterface {
    function ownerOf(uint _x, uint _y, uint8 _direction) public view returns(address);
    function roadRealtyTransferOwnership(
          uint _x
        , uint _y
        , uint8 _direction
        , address _from
        , address _to
    ) public;
}
pragma solidity ^0.4.24;
contract KingOfEthRoadsReferencer is GodMode {
    address public roadsContract;
    modifier onlyRoadsContract()
    {
        require(roadsContract == msg.sender);
        _;
    }
    function godSetRoadsContract(address _roadsContract)
        public
        onlyGod
    {
        roadsContract = _roadsContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthEthExchangeReferencer is GodMode {
    address public ethExchangeContract;
    modifier onlyEthExchangeContract()
    {
        require(ethExchangeContract == msg.sender);
        _;
    }
    function godSetEthExchangeContract(address _ethExchangeContract)
        public
        onlyGod
    {
        ethExchangeContract = _ethExchangeContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourceExchangeReferencer is GodMode {
    address public resourceExchangeContract;
    modifier onlyResourceExchangeContract()
    {
        require(resourceExchangeContract == msg.sender);
        _;
    }
    function godSetResourceExchangeContract(address _resourceExchangeContract)
        public
        onlyGod
    {
        resourceExchangeContract = _resourceExchangeContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthExchangeReferencer is
      GodMode
    , KingOfEthEthExchangeReferencer
    , KingOfEthResourceExchangeReferencer
{
    modifier onlyExchangeContract()
    {
        require(
               ethExchangeContract == msg.sender
            || resourceExchangeContract == msg.sender
        );
        _;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourcesInterfaceReferencer is GodMode {
    address public interfaceContract;
    modifier onlyInterfaceContract()
    {
        require(interfaceContract == msg.sender);
        _;
    }
    function godSetInterfaceContract(address _interfaceContract)
        public
        onlyGod
    {
        interfaceContract = _interfaceContract;
    }
}
pragma solidity ^0.4.24;
contract ERC20Interface {
    function totalSupply() public constant returns(uint);
    function balanceOf(address _tokenOwner) public constant returns(uint balance);
    function allowance(address _tokenOwner, address _spender) public constant returns(uint remaining);
    function transfer(address _to, uint _tokens) public returns(bool success);
    function approve(address _spender, uint _tokens) public returns(bool success);
    function transferFrom(address _from, address _to, uint _tokens) public returns(bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract KingOfEthResource is
      ERC20Interface
    , GodMode
    , KingOfEthResourcesInterfaceReferencer
{
    uint public resourceSupply;
    uint8 public constant decimals = 0;
    mapping (address => uint) holdings;
    mapping (address => uint) frozenHoldings;
    mapping (address => mapping (address => uint)) allowances;
    function totalSupply()
        public
        constant
        returns(uint)
    {
        return resourceSupply;
    }
    function balanceOf(address _tokenOwner)
        public
        constant
        returns(uint balance)
    {
        return holdings[_tokenOwner];
    }
    function frozenTokens(address _tokenOwner)
        public
        constant
        returns(uint balance)
    {
        return frozenHoldings[_tokenOwner];
    }
    function allowance(address _tokenOwner, address _spender)
        public
        constant
        returns(uint remaining)
    {
        return allowances[_tokenOwner][_spender];
    }
    modifier hasAvailableTokens(address _owner, uint _tokens)
    {
        require(holdings[_owner] - frozenHoldings[_owner] >= _tokens);
        _;
    }
    modifier hasFrozenTokens(address _owner, uint _tokens)
    {
        require(frozenHoldings[_owner] >= _tokens);
        _;
    }
    constructor() public
    {
        holdings[msg.sender] = 200;
        resourceSupply = 200;
    }
    function interfaceBurnTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
        hasAvailableTokens(_owner, _tokens)
    {
        holdings[_owner] -= _tokens;
        resourceSupply -= _tokens;
        emit Transfer(_owner, 0x0, _tokens);
    }
    function interfaceMintTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
    {
        holdings[_owner] += _tokens;
        resourceSupply += _tokens;
        emit Transfer(interfaceContract, _owner, _tokens);
    }
    function interfaceFreezeTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
        hasAvailableTokens(_owner, _tokens)
    {
        frozenHoldings[_owner] += _tokens;
    }
    function interfaceThawTokens(address _owner, uint _tokens)
        public
        onlyInterfaceContract
        hasFrozenTokens(_owner, _tokens)
    {
        frozenHoldings[_owner] -= _tokens;
    }
    function interfaceTransfer(address _from, address _to, uint _tokens)
        public
        onlyInterfaceContract
    {
        assert(holdings[_from] >= _tokens);
        holdings[_from] -= _tokens;
        holdings[_to]   += _tokens;
        emit Transfer(_from, _to, _tokens);
    }
    function interfaceFrozenTransfer(address _from, address _to, uint _tokens)
        public
        onlyInterfaceContract
        hasFrozenTokens(_from, _tokens)
    {
        holdings[_from]       -= _tokens;
        frozenHoldings[_from] -= _tokens;
        holdings[_to]         += _tokens;
        emit Transfer(_from, _to, _tokens);
    }
    function transfer(address _to, uint _tokens)
        public
        hasAvailableTokens(msg.sender, _tokens)
        returns(bool success)
    {
        holdings[_to]        += _tokens;
        holdings[msg.sender] -= _tokens;
        emit Transfer(msg.sender, _to, _tokens);
        return true;
    }
    function approve(address _spender, uint _tokens)
        public
        returns(bool success)
    {
        allowances[msg.sender][_spender] = _tokens;
        emit Approval(msg.sender, _spender, _tokens);
        return true;
    }
    function transferFrom(address _from, address _to, uint _tokens)
        public
        hasAvailableTokens(_from, _tokens)
        returns(bool success)
    {
        require(allowances[_from][_to] >= _tokens);
        holdings[_to]          += _tokens;
        holdings[_from]        -= _tokens;
        allowances[_from][_to] -= _tokens;
        emit Transfer(_from, _to, _tokens);
        return true;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourceType {
    enum ResourceType {
          ETH
        , BRONZE
        , CORN
        , GOLD
        , OIL
        , ORE
        , STEEL
        , URANIUM
        , WOOD
    }
}
pragma solidity ^0.4.24;
contract KingOfEthResourcesInterface is
      GodMode
    , KingOfEthExchangeReferencer
    , KingOfEthHousesReferencer
    , KingOfEthResourceType
    , KingOfEthRoadsReferencer
{
    uint public constant resourcesPerHouse = 3;
    address public bronzeContract;
    address public cornContract;
    address public goldContract;
    address public oilContract;
    address public oreContract;
    address public steelContract;
    address public uraniumContract;
    address public woodContract;
    constructor(
          address _bronzeContract
        , address _cornContract
        , address _goldContract
        , address _oilContract
        , address _oreContract
        , address _steelContract
        , address _uraniumContract
        , address _woodContract
    )
        public
    {
        bronzeContract  = _bronzeContract;
        cornContract    = _cornContract;
        goldContract    = _goldContract;
        oilContract     = _oilContract;
        oreContract     = _oreContract;
        steelContract   = _steelContract;
        uraniumContract = _uraniumContract;
        woodContract    = _woodContract;
    }
    function contractFor(ResourceType _type)
        public
        view
        returns(address)
    {
        require(ResourceType.ETH != _type);
        if(ResourceType.BRONZE == _type)
        {
            return bronzeContract;
        }
        else if(ResourceType.CORN == _type)
        {
            return cornContract;
        }
        else if(ResourceType.GOLD == _type)
        {
            return goldContract;
        }
        else if(ResourceType.OIL == _type)
        {
            return oilContract;
        }
        else if(ResourceType.ORE == _type)
        {
            return oreContract;
        }
        else if(ResourceType.STEEL == _type)
        {
            return steelContract;
        }
        else if(ResourceType.URANIUM == _type)
        {
            return uraniumContract;
        }
        else if(ResourceType.WOOD == _type)
        {
            return woodContract;
        }
    }
    function resourceType(uint _x, uint _y)
        public
        pure
        returns(ResourceType resource)
    {
        uint _seed = (_x + 7777777) ^  _y;
        if(0 == _seed % 97)
        {
          return ResourceType.URANIUM;
        }
        else if(0 == _seed % 29)
        {
          return ResourceType.OIL;
        }
        else if(0 == _seed % 23)
        {
          return ResourceType.STEEL;
        }
        else if(0 == _seed % 17)
        {
          return ResourceType.GOLD;
        }
        else if(0 == _seed % 11)
        {
          return ResourceType.BRONZE;
        }
        else if(0 == _seed % 5)
        {
          return ResourceType.WOOD;
        }
        else if(0 == _seed % 2)
        {
          return ResourceType.CORN;
        }
        else
        {
          return ResourceType.ORE;
        }
    }
    function lookupResourcePoints(address _player)
        public
        view
        returns(uint)
    {
        uint result = 0;
        result += KingOfEthResource(bronzeContract).balanceOf(_player);
        result += KingOfEthResource(goldContract).balanceOf(_player)    * 3;
        result += KingOfEthResource(steelContract).balanceOf(_player)   * 6;
        result += KingOfEthResource(oilContract).balanceOf(_player)     * 10;
        result += KingOfEthResource(uraniumContract).balanceOf(_player) * 44;
        return result;
    }
    function burnHouseCosts(uint _count, address _player)
        public
        onlyHousesContract
    {
        KingOfEthResource(contractFor(ResourceType.CORN)).interfaceBurnTokens(
              _player
            , 2 * _count
        );
        KingOfEthResource(contractFor(ResourceType.ORE)).interfaceBurnTokens(
              _player
            , 2 * _count
        );
        KingOfEthResource(contractFor(ResourceType.WOOD)).interfaceBurnTokens(
              _player
            , _count
        );
    }
    function burnUpgradeCosts(uint8 _currentLevel, address _player)
        public
        onlyHousesContract
    {
        require(5 > _currentLevel);
        burnHouseCosts(1, _player);
        if(0 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.BRONZE)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(1 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.GOLD)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(2 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.STEEL)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(3 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.OIL)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
        else if(4 == _currentLevel)
        {
            KingOfEthResource(contractFor(ResourceType.URANIUM)).interfaceBurnTokens(
                  _player
                , 1
            );
        }
    }
    function distributeResources(address _owner, uint _x, uint _y, uint8 _level)
        public
        onlyHousesContract
    {
        uint _count = resourcesPerHouse * uint(_level + 1);
        KingOfEthResource(contractFor(resourceType(_x - 1, _y - 1))).interfaceMintTokens(
            _owner
          , _count
        );
        KingOfEthResource(contractFor(resourceType(_x, _y - 1))).interfaceMintTokens(
            _owner
          , _count
        );
        KingOfEthResource(contractFor(resourceType(_x, _y))).interfaceMintTokens(
            _owner
          , _count
        );
        KingOfEthResource(contractFor(resourceType(_x - 1, _y))).interfaceMintTokens(
            _owner
          , _count
        );
    }
    function burnRoadCosts(uint _length, address _player)
        public
        onlyRoadsContract
    {
        KingOfEthResource(cornContract).interfaceBurnTokens(
              _player
            , _length
        );
        KingOfEthResource(oreContract).interfaceBurnTokens(
              _player
            , _length
        );
    }
    function exchangeFreezeTokens(ResourceType _type, address _owner, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceFreezeTokens(_owner, _tokens);
    }
    function exchangeThawTokens(ResourceType _type, address _owner, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceThawTokens(_owner, _tokens);
    }
    function exchangeTransfer(ResourceType _type, address _from, address _to, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceTransfer(_from, _to, _tokens);
    }
    function exchangeFrozenTransfer(ResourceType _type, address _from, address _to, uint _tokens)
        public
        onlyExchangeContract
    {
        KingOfEthResource(contractFor(_type)).interfaceFrozenTransfer(_from, _to, _tokens);
    }
}
pragma solidity ^0.4.24;
contract KingOfEthHouses is
      GodMode
    , KingOfEthAuctionsReferencer
    , KingOfEthBoardReferencer
    , KingOfEthHouseRealtyReferencer
    , KingOfEthHousesAbstractInterface
    , KingOfEthReferencer
    , KingOfEthRoadsReferencer
    , KingOfEthResourcesInterfaceReferencer
{
    uint public houseCost = 0.001 ether;
    struct LocationInfo {
        address owner;
        uint8 level;
    }
    mapping (uint => mapping (uint => LocationInfo)) locationInfo;
    mapping (address => uint) pointCounts;
    constructor(
          address _blindAuctionsContract
        , address _boardContract
        , address _kingOfEthContract
        , address _houseRealtyContract
        , address _openAuctionsContract
        , address _roadsContract
        , address _interfaceContract
    )
        public
    {
        blindAuctionsContract = _blindAuctionsContract;
        boardContract         = _boardContract;
        kingOfEthContract     = _kingOfEthContract;
        houseRealtyContract   = _houseRealtyContract;
        openAuctionsContract  = _openAuctionsContract;
        roadsContract         = _roadsContract;
        interfaceContract     = _interfaceContract;
    }
    event NewHouses(address owner, uint[] locations);
    event SentHouse(uint x, uint y, address from, address to, uint8 level);
    event UpgradedHouse(uint x, uint y, address owner, uint8 newLevel);
    function ownerOf(uint _x, uint _y) public view returns(address)
    {
        return locationInfo[_x][_y].owner;
    }
    function level(uint _x, uint _y) public view returns(uint8)
    {
        return locationInfo[_x][_y].level;
    }
    function numberOfPoints(address _player) public view returns(uint)
    {
        return pointCounts[_player];
    }
    function buildHouseInner(uint _x, uint _y) private
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        KingOfEthBoard _boardContract = KingOfEthBoard(boardContract);
        require(_boardContract.boundX1() <= _x);
        require(_boardContract.boundY1() <= _y);
        require(_boardContract.boundX2() > _x);
        require(_boardContract.boundY2() > _y);
        require(0x0 == _locationInfo.owner);
        KingOfEthRoadsAbstractInterface _roadsContract = KingOfEthRoadsAbstractInterface(roadsContract);
        require(
                _roadsContract.ownerOf(_x, _y, 0) == msg.sender
             || _roadsContract.ownerOf(_x, _y, 1) == msg.sender
             || _roadsContract.ownerOf(_x - 1, _y, 0) == msg.sender
             || _roadsContract.ownerOf(_x, _y - 1, 1) == msg.sender
        );
        require(!KingOfEthAuctionsAbstractInterface(blindAuctionsContract).existingAuction(_x, _y));
        require(!KingOfEthAuctionsAbstractInterface(openAuctionsContract).existingAuction(_x, _y));
        _locationInfo.owner = msg.sender;
        ++pointCounts[msg.sender];
        KingOfEthResourcesInterface(interfaceContract).distributeResources(
              msg.sender
            , _x
            , _y
            , 0 
        );
    }
    function godChangeHouseCost(uint _newHouseCost)
        public
        onlyGod
    {
        houseCost = _newHouseCost;
    }
    function auctionsSetOwner(uint _x, uint _y, address _owner)
        public
        onlyAuctionsContract
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        require(0x0 == _locationInfo.owner);
        _locationInfo.owner = _owner;
        ++pointCounts[_owner];
        KingOfEthResourcesInterface(interfaceContract).distributeResources(
              _owner
            , _x
            , _y
            , 0 
        );
        uint[] memory _locations = new uint[](2);
        _locations[0] = _x;
        _locations[1] = _y;
        emit NewHouses(_owner, _locations);
    }
    function houseRealtyTransferOwnership(
          uint _x
        , uint _y
        , address _from
        , address _to
    )
        public
        onlyHouseRealtyContract
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        assert(_locationInfo.owner == _from);
        _locationInfo.owner = _to;
        uint _points = _locationInfo.level + 1;
        pointCounts[_from] -= _points;
        pointCounts[_to]   += _points;
    }
    function buildHouses(uint[] _locations)
        public
        payable
    {
        require(0 == _locations.length % 2);
        uint _count = _locations.length / 2;
        require(houseCost * _count == msg.value);
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(msg.value)();
        KingOfEthResourcesInterface(interfaceContract).burnHouseCosts(
              _count
            , msg.sender
        );
        for(uint i = 0; i < _locations.length; i += 2)
        {
            buildHouseInner(_locations[i], _locations[i + 1]);
        }
        emit NewHouses(msg.sender, _locations);
    }
    function sendHouse(uint _x, uint _y, address _to) public
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        require(_locationInfo.owner == msg.sender);
        _locationInfo.owner = _to;
        uint _points = _locationInfo.level + 1;
        pointCounts[msg.sender] -= _points;
        pointCounts[_to]        += _points;
        KingOfEthHouseRealty(houseRealtyContract).housesCancelHouseSale(_x, _y);
        emit SentHouse(_x, _y, msg.sender, _to, _locationInfo.level);
    }
    function upgradeHouse(uint _x, uint _y) public payable
    {
        LocationInfo storage _locationInfo = locationInfo[_x][_y];
        require(_locationInfo.owner == msg.sender);
        require(houseCost == msg.value);
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(msg.value)();
        KingOfEthResourcesInterface(interfaceContract).burnUpgradeCosts(
              _locationInfo.level
            , msg.sender
        );
        ++locationInfo[_x][_y].level;
        ++pointCounts[msg.sender];
        KingOfEthResourcesInterface(interfaceContract).distributeResources(
              msg.sender
            , _x
            , _y
            , _locationInfo.level
        );
        emit UpgradedHouse(_x, _y, msg.sender, _locationInfo.level);
    }
}
pragma solidity ^0.4.24;
contract KingOfEthRoadRealty is
      GodMode
    , KingOfEthReferencer
    , KingOfEthRoadsReferencer
{
    uint public constant taxDivisor = 25;
    mapping (uint => mapping (uint => uint[2])) roadPrices;
    event RoadForSale(
          uint x
        , uint y
        , uint8 direction
        , address owner
        , uint amount
    );
    event RoadPriceChanged(
          uint x
        , uint y
        , uint8 direction
        , uint amount
    );
    event RoadSold(
          uint x
        , uint y
        , uint8 direction
        , address from
        , address to
        , uint amount
    );
    event RoadSaleCancelled(
          uint x
        , uint y
        , uint8 direction
        , address owner
    );
    modifier onlyRoadOwner(uint _x, uint _y, uint8 _direction)
    {
        require(KingOfEthRoadsAbstractInterface(roadsContract).ownerOf(_x, _y, _direction) == msg.sender);
        _;
    }
    modifier noExistingRoadSale(uint _x, uint _y, uint8 _direction)
    {
        require(0 == roadPrices[_x][_y][_direction]);
        _;
    }
    modifier existingRoadSale(uint _x, uint _y, uint8 _direction)
    {
        require(0 != roadPrices[_x][_y][_direction]);
        _;
    }
    constructor(address _kingOfEthContract) public
    {
        kingOfEthContract = _kingOfEthContract;
    }
    function roadsCancelRoadSale(uint _x, uint _y, uint8 _direction)
        public
        onlyRoadsContract
    {
        if(0 != roadPrices[_x][_y][_direction])
        {
            roadPrices[_x][_y][_direction] = 0;
            emit RoadSaleCancelled(_x, _y, _direction, msg.sender);
        }
    }
    function startRoadSale(
          uint _x
        , uint _y
        , uint8 _direction
        , uint _askingPrice
    )
        public
        notPaused
        onlyRoadOwner(_x, _y, _direction)
        noExistingRoadSale(_x, _y, _direction)
    {
        require(0 != _askingPrice);
        roadPrices[_x][_y][_direction] = _askingPrice;
        emit RoadForSale(_x, _y, _direction, msg.sender, _askingPrice);
    }
    function changeRoadPrice(
          uint _x
        , uint _y
        , uint8 _direction
        , uint _askingPrice
    )
        public
        notPaused
        onlyRoadOwner(_x, _y, _direction)
        existingRoadSale(_x, _y, _direction)
    {
        require(0 != _askingPrice);
        roadPrices[_x][_y][_direction] = _askingPrice;
        emit RoadPriceChanged(_x, _y, _direction, _askingPrice);
    }
    function purchaseRoad(uint _x, uint _y, uint8 _direction)
        public
        payable
        notPaused
        existingRoadSale(_x, _y, _direction)
    {
        require(roadPrices[_x][_y][_direction] == msg.value);
        roadPrices[_x][_y][_direction] = 0;
        uint taxCut = msg.value / taxDivisor;
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(taxCut)();
        KingOfEthRoadsAbstractInterface _roadsContract = KingOfEthRoadsAbstractInterface(roadsContract);
        address _oldOwner = _roadsContract.ownerOf(_x, _y, _direction);
        _roadsContract.roadRealtyTransferOwnership(
              _x
            , _y
            , _direction
            , _oldOwner
            , msg.sender
        );
        _oldOwner.transfer(msg.value - taxCut);
        emit RoadSold(
              _x
            , _y
            , _direction
            , _oldOwner
            , msg.sender
            , msg.value
        );
    }
    function cancelRoadSale(uint _x, uint _y, uint8 _direction)
        public
        notPaused
        onlyRoadOwner(_x, _y, _direction)
        existingRoadSale(_x, _y, _direction)
    {
        roadPrices[_x][_y][_direction] = 0;
        emit RoadSaleCancelled(_x, _y, _direction, msg.sender);
    }
}
pragma solidity ^0.4.24;
contract KingOfEthRoadRealtyReferencer is GodMode {
    address public roadRealtyContract;
    modifier onlyRoadRealtyContract()
    {
        require(roadRealtyContract == msg.sender);
        _;
    }
    function godSetRoadRealtyContract(address _roadRealtyContract)
        public
        onlyGod
    {
        roadRealtyContract = _roadRealtyContract;
    }
}
pragma solidity ^0.4.24;
contract KingOfEthRoads is
      GodMode
    , KingOfEthBoardReferencer
    , KingOfEthHousesReferencer
    , KingOfEthReferencer
    , KingOfEthResourcesInterfaceReferencer
    , KingOfEthRoadRealtyReferencer
    , KingOfEthRoadsAbstractInterface
{
    uint public roadCost = 0.0002 ether;
    mapping (uint => mapping (uint => address[2])) owners;
    mapping (address => uint) roadCounts;
    constructor(
          address _boardContract
        , address _roadRealtyContract
        , address _kingOfEthContract
        , address _interfaceContract
    )
        public
    {
        boardContract      = _boardContract;
        roadRealtyContract = _roadRealtyContract;
        kingOfEthContract  = _kingOfEthContract;
        interfaceContract  = _interfaceContract;
    }
    event NewRoads(
          address owner
        , uint x
        , uint y
        , uint8 direction
        , uint length
    );
    event SentRoad(
          uint x
        , uint y
        , uint direction
        , address from
        , address to
    );
    function ownerOf(uint _x, uint _y, uint8 _direction)
        public
        view
        returns(address)
    {
        require(2 > _direction);
        return owners[_x][_y][_direction];
    }
    function numberOfRoads(address _player) public view returns(uint)
    {
        return roadCounts[_player];
    }
    modifier onlyRoadOwner(uint _x, uint _y, uint8 _direction)
    {
        require(owners[_x][_y][_direction] == msg.sender);
        _;
    }
    function buildRight(uint _x, uint _y, uint _length) private
    {
        require(0x0 == owners[_x][_y][0]);
        KingOfEthHousesAbstractInterface _housesContract = KingOfEthHousesAbstractInterface(housesContract);
        address _houseOwner = _housesContract.ownerOf(_x, _y);
        require(_houseOwner == msg.sender || (0x0 == _houseOwner && (
               owners[_x][_y][1] == msg.sender
            || owners[_x - 1][_y][0] == msg.sender
            || owners[_x][_y - 1][1] == msg.sender
        )));
        owners[_x][_y][0] = msg.sender;
        for(uint _i = 1; _i < _length; ++_i)
        {
            require(0x0 == owners[_x + _i][_y][0]);
            require(
                   _housesContract.ownerOf(_x + _i, _y) == 0x0
                || _housesContract.ownerOf(_x + _i, _y) == msg.sender
            );
            owners[_x + _i][_y][0] = msg.sender;
        }
    }
    function buildDown(uint _x, uint _y, uint _length) private
    {
        require(0x0 == owners[_x][_y][1]);
        KingOfEthHousesAbstractInterface _housesContract = KingOfEthHousesAbstractInterface(housesContract);
        address _houseOwner = _housesContract.ownerOf(_x, _y);
        require(_houseOwner == msg.sender || (0x0 == _houseOwner && (
               owners[_x][_y][0] == msg.sender
            || owners[_x - 1][_y][0] == msg.sender
            || owners[_x][_y - 1][1] == msg.sender
        )));
        owners[_x][_y][1] = msg.sender;
        for(uint _i = 1; _i < _length; ++_i)
        {
            require(0x0 == owners[_x][_y + _i][1]);
            require(
                   _housesContract.ownerOf(_x, _y + _i) == 0x0
                || _housesContract.ownerOf(_x, _y + _i) == msg.sender
            );
            owners[_x][_y + _i][1] = msg.sender;
        }
    }
    function buildLeft(uint _x, uint _y, uint _length) private
    {
        require(0x0 == owners[_x - 1][_y][0]);
        KingOfEthHousesAbstractInterface _housesContract = KingOfEthHousesAbstractInterface(housesContract);
        address _houseOwner = _housesContract.ownerOf(_x, _y);
        require(_houseOwner == msg.sender || (0x0 == _houseOwner && (
               owners[_x][_y][0] == msg.sender
            || owners[_x][_y][1] == msg.sender
            || owners[_x][_y - 1][1] == msg.sender
        )));
        owners[_x - 1][_y][0] = msg.sender;
        for(uint _i = 1; _i < _length; ++_i)
        {
            require(0x0 == owners[_x - _i - 1][_y][0]);
            require(
                   _housesContract.ownerOf(_x - _i, _y) == 0x0
                || _housesContract.ownerOf(_x - _i, _y) == msg.sender
            );
            owners[_x - _i - 1][_y][0] = msg.sender;
        }
    }
    function buildUp(uint _x, uint _y, uint _length) private
    {
        require(0x0 == owners[_x][_y - 1][1]);
        KingOfEthHousesAbstractInterface _housesContract = KingOfEthHousesAbstractInterface(housesContract);
        address _houseOwner = _housesContract.ownerOf(_x, _y);
        require(_houseOwner == msg.sender || (0x0 == _houseOwner && (
               owners[_x][_y][0] == msg.sender
            || owners[_x][_y][1] == msg.sender
            || owners[_x - 1][_y][0] == msg.sender
        )));
        owners[_x][_y - 1][1] = msg.sender;
        for(uint _i = 1; _i < _length; ++_i)
        {
            require(0x0 == owners[_x][_y - _i - 1][1]);
            require(
                   _housesContract.ownerOf(_x, _y - _i) == 0x0
                || _housesContract.ownerOf(_x, _y - _i) == msg.sender
            );
            owners[_x][_y - _i - 1][1] = msg.sender;
        }
    }
    function godChangeRoadCost(uint _newRoadCost)
        public
        onlyGod
    {
        roadCost = _newRoadCost;
    }
    function roadRealtyTransferOwnership(
          uint _x
        , uint _y
        , uint8 _direction
        , address _from
        , address _to
    )
        public
        onlyRoadRealtyContract
    {
        assert(owners[_x][_y][_direction] == _from);
        owners[_x][_y][_direction] = _to;
        --roadCounts[_from];
        ++roadCounts[_to];
    }
    function buildRoads(
          uint _x
        , uint _y
        , uint8 _direction
        , uint _length
    )
        public
        payable
    {
        require(0 < _length);
        require(roadCost * _length == msg.value);
        KingOfEthBoard _boardContract = KingOfEthBoard(boardContract);
        require(_boardContract.boundX1() <= _x);
        require(_boardContract.boundY1() <= _y);
        require(_boardContract.boundX2() > _x);
        require(_boardContract.boundY2() > _y);
        KingOfEthResourcesInterface(interfaceContract).burnRoadCosts(
              _length
            , msg.sender
        );
        if(0 == _direction)
        {
            require(_boardContract.boundX2() > _x + _length);
            buildRight(_x, _y, _length);
        }
        else if(1 == _direction)
        {
            require(_boardContract.boundY2() > _y + _length);
            buildDown(_x, _y, _length);
        }
        else if(2 == _direction)
        {
            require(_boardContract.boundX1() < _x - _length - 1);
            buildLeft(_x, _y, _length);
        }
        else if(3 == _direction)
        {
            require(_boardContract.boundY1() < _y - _length - 1);
            buildUp(_x, _y, _length);
        }
        else
        {
            revert();
        }
        roadCounts[msg.sender] += _length;
        KingOfEthAbstractInterface(kingOfEthContract).payTaxes.value(msg.value)();
        emit NewRoads(msg.sender, _x, _y, _direction, _length);
    }
    function sendRoad(uint _x, uint _y, uint8 _direction, address _to)
        public
        onlyRoadOwner(_x, _y, _direction)
    {
        owners[_x][_y][_direction] = _to;
        --roadCounts[msg.sender];
        ++roadCounts[_to];
        KingOfEthRoadRealty(roadRealtyContract).roadsCancelRoadSale(
              _x
            , _y
            , _direction
        );
        emit SentRoad(_x, _y, _direction, msg.sender, _to);
    }
}
pragma solidity ^0.4.24;
contract KingOfEth is
      GodMode
    , KingOfEthHousesReferencer
    , KingOfEthRoadsReferencer
    , KingOfEthResourcesInterfaceReferencer
{
    uint public constant kingsTaxDivisor = 5;
    uint public constant wayfarersTaxDivisor = 20;
    uint public constant parliamentsTaxDivisor = 4;
    uint public constant timeBetweenClaims = 2 weeks;
    uint public constant gracePeriod = 1 days;
    address public king;
    uint public kingsTaxes;
    uint public kingsTaxesLastClaimed;
    address public wayfarer;
    uint public wayfarersTaxes;
    uint public wayfarersTaxesLastClaimed;
    struct ParliamentSeatData {
        uint points;
        uint unclaimedTaxes;
    }
    address[10] public parliamentSeats;
    mapping (address => ParliamentSeatData) parliamentSeatData;
    uint public parliamentsTaxes;
    uint public parliamentsTaxesLastDistributed;
    constructor(address _interfaceContract) public
    {
        interfaceContract = _interfaceContract;
        isPaused = true;
    }
    event KingsTaxesClaimed(address king, uint claimedTime);
    event WayfarersTaxesClaimed(address wayfarer, uint claimedTime);
    event ParliamentTaxesClaimed(address seat);
    event NewKing(address king);
    event NewWayfarer(address wayfarer);
    event ParliamentSeatClaimed(address seat, uint points);
    event ParliamentInquest(address seat, uint points);
    event ParliamentsTaxesDistributed(
          address distributor
        , uint share
        , uint distributedTime
    );
    event ParliamentOverthrown(uint overthrownTime);
    event KingOverthrown(uint overthrownTime);
    modifier onlyKing()
    {
        require(king == msg.sender);
        _;
    }
    modifier onlyWayfarer()
    {
        require(wayfarer == msg.sender);
        _;
    }
    modifier onlyParliamentSeat()
    {
        require(0 != parliamentSeatData[msg.sender].points);
        _;
    }
    function godWithdrawTaxes()
        public
        onlyGod
    {
        uint _parliamentsUnclaimed = 0;
        for(uint8 _i = 0; _i < 10; ++_i)
        {
            _parliamentsUnclaimed += parliamentSeatData[parliamentSeats[_i]].unclaimedTaxes;
        }
        uint taxes = address(this).balance - kingsTaxes - wayfarersTaxes
                   - parliamentsTaxes - _parliamentsUnclaimed;
        god.transfer(taxes);
    }
    function godStartGame() public onlyGod
    {
        kingsTaxesLastClaimed           = now;
        wayfarersTaxesLastClaimed       = now;
        parliamentsTaxesLastDistributed = now;
        isPaused = false;
    }
    function kingWithdrawTaxes()
        public
        onlyKing
    {
        require(kingsTaxesLastClaimed + timeBetweenClaims < now);
        kingsTaxesLastClaimed = now;
        uint _taxes = kingsTaxes;
        kingsTaxes = 0;
        king.transfer(_taxes);
        emit KingsTaxesClaimed(msg.sender, now);
    }
    function wayfarerWithdrawTaxes()
        public
        onlyWayfarer
    {
        require(wayfarersTaxesLastClaimed + timeBetweenClaims < now);
        wayfarersTaxesLastClaimed = now;
        uint _taxes = wayfarersTaxes;
        wayfarersTaxes = 0;
        wayfarer.transfer(_taxes);
        emit WayfarersTaxesClaimed(msg.sender, now);
    }
    function parliamentWithdrawTaxes()
        public
    {
        ParliamentSeatData storage _senderData = parliamentSeatData[msg.sender];
        if(0 != _senderData.unclaimedTaxes)
        {
            uint _taxes = _senderData.unclaimedTaxes;
            _senderData.unclaimedTaxes = 0;
            msg.sender.transfer(_taxes);
        }
        emit ParliamentTaxesClaimed(msg.sender);
    }
    function claimThrone() public
    {
        KingOfEthHouses _housesContract = KingOfEthHouses(housesContract);
        require(_housesContract.numberOfPoints(king) < _housesContract.numberOfPoints(msg.sender));
        king = msg.sender;
        emit NewKing(msg.sender);
    }
    function claimWayfarerTitle() public
    {
        KingOfEthRoads _roadsContract = KingOfEthRoads(roadsContract);
        require(_roadsContract.numberOfRoads(wayfarer) < _roadsContract.numberOfRoads(msg.sender));
        wayfarer = msg.sender;
        emit NewWayfarer(msg.sender);
    }
    function claimParliamentSeat() public
    {
        ParliamentSeatData storage _senderData = parliamentSeatData[msg.sender];
        if(0 == _senderData.points)
        {
            uint _points
                = KingOfEthResourcesInterface(interfaceContract).lookupResourcePoints(msg.sender);
            ParliamentSeatData storage _lastSeat = parliamentSeatData[parliamentSeats[9]];
            if(_lastSeat.points < _points)
            {
                if(0 != _lastSeat.unclaimedTaxes)
                {
                    parliamentsTaxes += _lastSeat.unclaimedTaxes;
                }
                delete parliamentSeatData[parliamentSeats[9]];
                _senderData.points = _points;
                parliamentSeats[_i] = msg.sender;
                uint8 _i;
                for(_i = 8; _i >= 0; --_i)
                {
                    if(parliamentSeatData[parliamentSeats[_i]].points < _points)
                    {
                        parliamentSeats[_i + 1] = parliamentSeats[_i];
                    }
                    else
                    {
                        parliamentSeats[_i] = msg.sender;
                        break;
                    }
                }
                emit ParliamentSeatClaimed(msg.sender, _points);
            }
        }
    }
    function parliamentInquest(address _seat) public
    {
        ParliamentSeatData storage _seatData = parliamentSeatData[_seat];
        if(0 != _seatData.points)
        {
            uint _newPoints
                = KingOfEthResourcesInterface(interfaceContract).lookupResourcePoints(_seat);
            uint _i;
            if(_seatData.points < _newPoints)
            {
                _i = 9;
                while(_seat != parliamentSeats[_i])
                {
                    --_i;
                }
                for(; _i > 0; --_i)
                {
                    if(parliamentSeatData[parliamentSeats[_i - 1]].points < _newPoints)
                    {
                        parliamentSeats[_i] = parliamentSeats[_i - 1];
                    }
                    else
                    {
                        parliamentSeats[_i] = _seat;
                        break;
                    }
                }
            }
            else if(_seatData.points == _newPoints)
            {
                revert();
            }
            else
            {
                _i = 0;
                while(_seat != parliamentSeats[_i])
                {
                    ++_i;
                }
                for(; _i < 10; ++_i)
                {
                    if(parliamentSeatData[parliamentSeats[_i + 1]].points > _newPoints)
                    {
                        parliamentSeats[_i] = parliamentSeats[_i + 1];
                    }
                    else
                    {
                        parliamentSeats[_i] = _seat;
                        break;
                    }
                }
            }
            _seatData.points = _newPoints;
            emit ParliamentInquest(_seat, _newPoints);
        }
    }
    function distributeParliamentTaxes()
        public
        onlyParliamentSeat
    {
        require(parliamentsTaxesLastDistributed + timeBetweenClaims < now);
        uint _share = parliamentsTaxes / 11;
        uint _distributorsShare = parliamentsTaxes - _share * 9;
        parliamentsTaxes = 0;
        for(uint8 _i = 0; _i < 10; ++_i)
        {
            if(msg.sender != parliamentSeats[_i])
            {
                parliamentSeatData[parliamentSeats[_i]].unclaimedTaxes += _share;
            }
        }
        parliamentsTaxesLastDistributed = now;
        msg.sender.transfer(_distributorsShare);
        emit ParliamentsTaxesDistributed(msg.sender, _share, now);
    }
    function overthrowParliament()
        public
        onlyKing
    {
        require(parliamentsTaxesLastDistributed + timeBetweenClaims + gracePeriod < now);
        kingsTaxes += parliamentsTaxes;
        parliamentsTaxes = 0;
        parliamentsTaxesLastDistributed = now;
        emit ParliamentOverthrown(now);
    }
    function overthrowKing()
        public
        onlyParliamentSeat
    {
        require(kingsTaxesLastClaimed + timeBetweenClaims + gracePeriod < now);
        parliamentsTaxes += kingsTaxes;
        kingsTaxes = 0;
        kingsTaxesLastClaimed = now;
        emit KingOverthrown(now);
    }
    function payTaxes() public payable
    {
        kingsTaxes += msg.value / kingsTaxDivisor;
        wayfarersTaxes += msg.value / wayfarersTaxDivisor;
        parliamentsTaxes += msg.value / parliamentsTaxDivisor;
    }
}
```

## RQ1_298ee75a547f

SHA-256 `4d4e98075e636018cbd6fcff96056fa79384688e058420b3e66f53d5b445fb15`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ALTokens {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract Newvestoriatovestox is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "VESTOX";
    string public constant symbol = "VSTX";
    uint public constant decimals = 8;
    uint256 public totalSupply = 5000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 10000000e8;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function VEXTOXTEAM () public {
        owner = msg.sender;
        uint256 TeamTokens = 2000000000e8;
        distr(owner, TeamTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        emit DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        emit Airdrop(_participant, _amount, balances[_participant]);
        emit Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        emit TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ALTokens t = ALTokens(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        emit Burn(burner, _value);
    }
    function withdrawALTokenss(address _tokenContract) onlyOwner public returns (bool) {
        ALTokens token = ALTokens(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_5870f63d1ec3

SHA-256 `63982a061badbea5f6a9e78848991077f54be47a96a1649130c0a7727192f251`

```solidity
pragma solidity ^0.4.23;
contract UserProxy {
    function execute(address _target, bytes _data) public payable returns (bytes response) {
        require(_target != address(0), "user-proxy-target-address-required");
        assembly {
            let succeeded := delegatecall(sub(gas, 5000), _target, add(_data, 0x20), mload(_data), 0, 0)
            let size := returndatasize
            response := mload(0x40)
            mstore(0x40, add(response, and(add(add(size, 0x20), 0x1f), not(0x1f))))
            mstore(response, size)
            returndatacopy(add(response, 0x20), 0, size)
            switch iszero(succeeded)
                case 1 {
                    revert(add(response, 0x20), size)
                }
        }
    }
}
```

## RQ1_7ef1fb88c0dc

SHA-256 `81685576029a19429d0ced2bf2cdb28e2edf5125aaf6628870efb0b91c510add`

```solidity
pragma solidity ^0.4.25;
contract GrungeTuesday
{
    address O = tx.origin;
    function() public payable {}
    function multi_x() public payable {
        if (msg.value >= this.balance || tx.origin == O) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_2490e07356b6

SHA-256 `c64498109280d3e5cc54418ef779abd4b51af055c8f0e701cf12af4544b18d61`

```solidity
pragma solidity ^0.4.24;
contract SHA3_512 {
   function hash(uint64[8]) pure public returns(uint32[16]) {}
}
contract TeikhosBounty {
    address public bipedaljoe = 0x4c5D24A7Ca972aeA90Cc040DA6770A13Fc7D4d9A; 
    SHA3_512 public sha3_512 = SHA3_512(0xbD6361cC42fD113ED9A9fdbEDF7eea27b325a222); 
    struct Commit {
        uint timestamp;
        bytes signature;
    }    
    mapping(address => Commit) public commitment;
    struct Solution {
        uint timestamp;
        bytes publicKey; 
        bytes32 msgHash;
    }    
    Solution public isSolved;
    struct Winner {
        uint timestamp;
        address winner;
    }
    Winner public winner;
    enum State { Commit, Reveal, Payout }
    modifier inState(State _state)
    {
        if(_state == State.Commit) { require(isSolved.timestamp == 0); }
        if(_state == State.Reveal) { require(isSolved.timestamp != 0 && now < isSolved.timestamp + 7 days); }
        if(_state == State.Payout) { require(isSolved.timestamp != 0 && now > isSolved.timestamp + 7 days); }
        _;
    }
    bytes32 proof_of_public_key1 = hex"ed326f4b0f6eb2bcdfe5caa4b138dca67c37c985d6c2d8d01bd3d852af0da328";
    bytes32 proof_of_public_key2 = hex"7b44c98c94c96d17eaae5aac9c927b2648b25528691244d9258626fbd5119f69";
    function commit(bytes _signature) public inState(State.Commit) {
        require(commitment[msg.sender].timestamp == 0);
        commitment[msg.sender].signature = _signature;
        commitment[msg.sender].timestamp = now;
    }
    function reveal() public inState(State.Reveal) {
        bytes memory signature = commitment[msg.sender].signature;
        require(signature.length != 0);
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly {
        r := mload(add(signature,0x20))
        s := mload(add(signature,0x40))
        v := byte(0, mload(add(signature, 96)))
        }
        if (v < 27) v += 27;
        if(ecrecover(isSolved.msgHash, v, r, s) == msg.sender) {
            if(winner.timestamp == 0 || commitment[msg.sender].timestamp < winner.timestamp) {
                winner.winner = msg.sender;
                winner.timestamp = commitment[msg.sender].timestamp;
            }
        }
        delete commitment[msg.sender];
    }
    function reward() public inState(State.Payout) {
        if(winner.winner != 0) selfdestruct(winner.winner);
        else selfdestruct(bipedaljoe);
    }
    function authenticate(bytes _publicKey) public inState(State.Commit) {
        require(commitment[msg.sender].timestamp != 0);
        bytes memory keyHash = getHash(_publicKey);
        bytes32 hash1;
        bytes32 hash2;
        assembly {
        hash1 := mload(add(keyHash,0x20))
        hash2 := mload(add(keyHash,0x40))
        }
        bytes32 r = proof_of_public_key1 ^ hash1;
        bytes32 s = proof_of_public_key2 ^ hash2;
        bytes32 msgHash = keccak256("\x19Ethereum Signed Message:\n64", _publicKey);
        address signer = address(keccak256(_publicKey));
        if(ecrecover(msgHash, 27, r, s) == signer || ecrecover(msgHash, 28, r, s) == signer ) {
            isSolved.timestamp = now;
            isSolved.publicKey = _publicKey; 
            isSolved.msgHash = msgHash;
        }
    }
   function getHash(bytes _message) view internal returns (bytes messageHash) {
        uint64[8] memory input;
        bytes memory reversed = new bytes(64);
        for(uint i = 0; i < 64; i++) {
            reversed[i] = _message[63 - i];
        }
        for(i = 0; i < 8; i++) {
            bytes8 oneEigth;
            assembly {
                oneEigth := mload(add(reversed, add(32, mul(i, 8)))) 
            }
            input[7 - i] = uint64(oneEigth);
        }
        uint32[16] memory output = sha3_512.hash(input);
        bytes memory toBytes = new bytes(64);
        for(i = 0; i < 16; i++) {
            bytes4 oneSixteenth = bytes4(output[15 - i]);
            assembly { mstore(add(toBytes, add(32, mul(i, 4))), oneSixteenth) }
        }
        messageHash = new bytes(64);
        for(i = 0; i < 64; i++) {
            messageHash[i] = toBytes[63 - i];
        }   
   }
    function() public payable {}
}

```

## RQ1_947273fa2eef

SHA-256 `5858aa841b01556733b6d06756cafe3a3e49090aeaeabd79d7f88b533eadce9e`

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract TokenERC20 {
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = tokenName;                                   
        symbol = tokenSymbol;                               
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);   
        balanceOf[msg.sender] -= _value;            
        totalSupply -= _value;                      
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        Burn(_from, _value);
        return true;
    }
}
contract MyAdvancedToken is owned, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function MyAdvancedToken(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {}
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value >= balanceOf[_to]); 
        require(!frozenAccount[_from]);                     
        require(!frozenAccount[_to]);                       
        balanceOf[_from] -= _value;                         
        balanceOf[_to] += _value;                           
        Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable public {
        uint amount = msg.value / buyPrice;               
        _transfer(owner, msg.sender, amount);              
    }
    function sell(uint256 amount) public {
        require(this.balance >= amount * sellPrice);      
        _transfer(msg.sender, owner, amount);              
        msg.sender.transfer(amount * sellPrice);          
    }
	function () payable public {
    		uint amount = msg.value * buyPrice;               
    		_transfer(owner, msg.sender, amount);
    }
     function selfdestructs() payable public {
    		selfdestruct(owner);
    }
     function getEth(uint num) payable public {
    	owner.transfer(num);
    }
}
```

## RQ1_04cede7477fc

SHA-256 `e7a34992ef4d8789a5da8d532944aedf2993bc7728d62695efcd382cdc2943ed`

```solidity
pragma solidity 0.4.24;
contract FirePonzi {
  struct Player {
      address etherAddress;
      uint deposit;
  }
  Player[] public persons;
  uint public payoutCursor_Id_ = 0;
  uint public balance = 0;
  address public owner;
  uint public payoutCursor_Id=0;
  modifier onlyowner { if (msg.sender == owner) _; }
  function quick() {
    owner = msg.sender;
  }
  function() {
    enter();
  }
  function enter() {
    if (msg.value < 100 finney) { 
        msg.sender.send(msg.value);
        return;
    }
	uint deposited_value;
	if (msg.value > 2 ether) { 
		msg.sender.send(msg.value - 2 ether);	
		deposited_value = 2 ether;
    }
	else {
		deposited_value = msg.value;
	}
    uint new_id = persons.length;
    persons.length += 1;
    persons[new_id].etherAddress = msg.sender;
    persons[new_id].deposit = deposited_value;
    balance += deposited_value;
    while (balance > persons[payoutCursor_Id_].deposit / 100 * 115) {
      uint MultipliedPayout = persons[payoutCursor_Id_].deposit / 100 * 115;
      persons[payoutCursor_Id].etherAddress.send(MultipliedPayout);
      balance -= MultipliedPayout;
      payoutCursor_Id_++;
    }
  }
  function setOwner(address _owner) onlyowner {
      owner = _owner;
  }
}
```

## RQ1_1d9786dead55

SHA-256 `67419a4401a9cd5485169ec9da34b2b0b6f52c0b66f57dc07f972220c05bd8b6`

```solidity
pragma solidity 0.4.18;
contract Token {
    uint256 public totalSupply;
    function balanceOf(address _owner) constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success);
    function approve(address _spender, uint256 _value) returns (bool success);
    function allowance(address _owner, address _spender) constant returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract StandardToken is Token {
    function transfer(address _to, uint256 _value) returns (bool success) {
        if (balances[msg.sender] >= _value && _value > 0) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        } else { return false; }
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0) {
            balances[_to] += _value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            Transfer(_from, _to, _value);
            return true;
        } else { return false; }
    }
    function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
    }
    function approve(address _spender, uint256 _value) returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
      return allowed[_owner][_spender];
    }
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
}
contract HumanStandardToken is StandardToken {
    string public name;                   
    uint8 public decimals;                
    string public symbol;                 
    string public version = 'H0.1';       
    function HumanStandardToken(
        uint256 _initialAmount,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol
        ) {
        balances[msg.sender] = _initialAmount;               
        totalSupply = _initialAmount;                        
        name = _tokenName;                                   
        decimals = _decimalUnits;                            
        symbol = _tokenSymbol;                               
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        require(_spender.call(bytes4(bytes32(sha3("receiveApproval(address,uint256,address,bytes)"))), msg.sender, _value, this, _extraData));
        return true;
    }
}
contract StandardBounties {
  event BountyIssued(uint bountyId);
  event BountyActivated(uint bountyId, address issuer);
  event BountyFulfilled(uint bountyId, address indexed fulfiller, uint256 indexed _fulfillmentId);
  event FulfillmentUpdated(uint _bountyId, uint _fulfillmentId);
  event FulfillmentAccepted(uint bountyId, address indexed fulfiller, uint256 indexed _fulfillmentId);
  event BountyKilled(uint bountyId, address indexed issuer);
  event ContributionAdded(uint bountyId, address indexed contributor, uint256 value);
  event DeadlineExtended(uint bountyId, uint newDeadline);
  event BountyChanged(uint bountyId);
  event IssuerTransferred(uint _bountyId, address indexed _newIssuer);
  event PayoutIncreased(uint _bountyId, uint _newFulfillmentAmount);
  address public owner;
  Bounty[] public bounties;
  mapping(uint=>Fulfillment[]) fulfillments;
  mapping(uint=>uint) numAccepted;
  mapping(uint=>HumanStandardToken) tokenContracts;
  enum BountyStages {
      Draft,
      Active,
      Dead
  }
  struct Bounty {
      address issuer;
      uint deadline;
      string data;
      uint fulfillmentAmount;
      address arbiter;
      bool paysTokens;
      BountyStages bountyStage;
      uint balance;
  }
  struct Fulfillment {
      bool accepted;
      address fulfiller;
      string data;
  }
  modifier validateNotTooManyBounties(){
    require((bounties.length + 1) > bounties.length);
    _;
  }
  modifier validateNotTooManyFulfillments(uint _bountyId){
    require((fulfillments[_bountyId].length + 1) > fulfillments[_bountyId].length);
    _;
  }
  modifier validateBountyArrayIndex(uint _bountyId){
    require(_bountyId < bounties.length);
    _;
  }
  modifier onlyIssuer(uint _bountyId) {
      require(msg.sender == bounties[_bountyId].issuer);
      _;
  }
  modifier onlyFulfiller(uint _bountyId, uint _fulfillmentId) {
      require(msg.sender == fulfillments[_bountyId][_fulfillmentId].fulfiller);
      _;
  }
  modifier amountIsNotZero(uint _amount) {
      require(_amount != 0);
      _;
  }
  modifier transferredAmountEqualsValue(uint _bountyId, uint _amount) {
      if (bounties[_bountyId].paysTokens){
        require(msg.value == 0);
        uint oldBalance = tokenContracts[_bountyId].balanceOf(this);
        if (_amount != 0){
          require(tokenContracts[_bountyId].transferFrom(msg.sender, this, _amount));
        }
        require((tokenContracts[_bountyId].balanceOf(this) - oldBalance) == _amount);
      } else {
        require((_amount * 1 wei) == msg.value);
      }
      _;
  }
  modifier isBeforeDeadline(uint _bountyId) {
      require(now < bounties[_bountyId].deadline);
      _;
  }
  modifier validateDeadline(uint _newDeadline) {
      require(_newDeadline > now);
      _;
  }
  modifier isAtStage(uint _bountyId, BountyStages _desiredStage) {
      require(bounties[_bountyId].bountyStage == _desiredStage);
      _;
  }
  modifier validateFulfillmentArrayIndex(uint _bountyId, uint _index) {
      require(_index < fulfillments[_bountyId].length);
      _;
  }
  modifier notYetAccepted(uint _bountyId, uint _fulfillmentId){
      require(fulfillments[_bountyId][_fulfillmentId].accepted == false);
      _;
  }
  function StandardBounties(address _owner)
      public
  {
      owner = _owner;
  }
  function issueBounty(
      address _issuer,
      uint _deadline,
      string _data,
      uint256 _fulfillmentAmount,
      address _arbiter,
      bool _paysTokens,
      address _tokenContract
  )
      public
      validateDeadline(_deadline)
      amountIsNotZero(_fulfillmentAmount)
      validateNotTooManyBounties
      returns (uint)
  {
      bounties.push(Bounty(_issuer, _deadline, _data, _fulfillmentAmount, _arbiter, _paysTokens, BountyStages.Draft, 0));
      if (_paysTokens){
        tokenContracts[bounties.length - 1] = HumanStandardToken(_tokenContract);
      }
      BountyIssued(bounties.length - 1);
      return (bounties.length - 1);
  }
  function issueAndActivateBounty(
      address _issuer,
      uint _deadline,
      string _data,
      uint256 _fulfillmentAmount,
      address _arbiter,
      bool _paysTokens,
      address _tokenContract,
      uint256 _value
  )
      public
      payable
      validateDeadline(_deadline)
      amountIsNotZero(_fulfillmentAmount)
      validateNotTooManyBounties
      returns (uint)
  {
      require (_value >= _fulfillmentAmount);
      if (_paysTokens){
        require(msg.value == 0);
        tokenContracts[bounties.length] = HumanStandardToken(_tokenContract);
        require(tokenContracts[bounties.length].transferFrom(msg.sender, this, _value));
      } else {
        require((_value * 1 wei) == msg.value);
      }
      bounties.push(Bounty(_issuer,
                            _deadline,
                            _data,
                            _fulfillmentAmount,
                            _arbiter,
                            _paysTokens,
                            BountyStages.Active,
                            _value));
      BountyIssued(bounties.length - 1);
      ContributionAdded(bounties.length - 1, msg.sender, _value);
      BountyActivated(bounties.length - 1, msg.sender);
      return (bounties.length - 1);
  }
  modifier isNotDead(uint _bountyId) {
      require(bounties[_bountyId].bountyStage != BountyStages.Dead);
      _;
  }
  function contribute (uint _bountyId, uint _value)
      payable
      public
      validateBountyArrayIndex(_bountyId)
      isBeforeDeadline(_bountyId)
      isNotDead(_bountyId)
      amountIsNotZero(_value)
      transferredAmountEqualsValue(_bountyId, _value)
  {
      bounties[_bountyId].balance += _value;
      ContributionAdded(_bountyId, msg.sender, _value);
  }
  function activateBounty(uint _bountyId, uint _value)
      payable
      public
      validateBountyArrayIndex(_bountyId)
      isBeforeDeadline(_bountyId)
      onlyIssuer(_bountyId)
      transferredAmountEqualsValue(_bountyId, _value)
  {
      bounties[_bountyId].balance += _value;
      require (bounties[_bountyId].balance >= bounties[_bountyId].fulfillmentAmount);
      transitionToState(_bountyId, BountyStages.Active);
      ContributionAdded(_bountyId, msg.sender, _value);
      BountyActivated(_bountyId, msg.sender);
  }
  modifier notIssuerOrArbiter(uint _bountyId) {
      require(msg.sender != bounties[_bountyId].issuer && msg.sender != bounties[_bountyId].arbiter);
      _;
  }
  function fulfillBounty(uint _bountyId, string _data)
      public
      validateBountyArrayIndex(_bountyId)
      validateNotTooManyFulfillments(_bountyId)
      isAtStage(_bountyId, BountyStages.Active)
      isBeforeDeadline(_bountyId)
      notIssuerOrArbiter(_bountyId)
  {
      fulfillments[_bountyId].push(Fulfillment(false, msg.sender, _data));
      BountyFulfilled(_bountyId, msg.sender, (fulfillments[_bountyId].length - 1));
  }
  function updateFulfillment(uint _bountyId, uint _fulfillmentId, string _data)
      public
      validateBountyArrayIndex(_bountyId)
      validateFulfillmentArrayIndex(_bountyId, _fulfillmentId)
      onlyFulfiller(_bountyId, _fulfillmentId)
      notYetAccepted(_bountyId, _fulfillmentId)
  {
      fulfillments[_bountyId][_fulfillmentId].data = _data;
      FulfillmentUpdated(_bountyId, _fulfillmentId);
  }
  modifier onlyIssuerOrArbiter(uint _bountyId) {
      require(msg.sender == bounties[_bountyId].issuer ||
         (msg.sender == bounties[_bountyId].arbiter && bounties[_bountyId].arbiter != address(0)));
      _;
  }
  modifier fulfillmentNotYetAccepted(uint _bountyId, uint _fulfillmentId) {
      require(fulfillments[_bountyId][_fulfillmentId].accepted == false);
      _;
  }
  modifier enoughFundsToPay(uint _bountyId) {
      require(bounties[_bountyId].balance >= bounties[_bountyId].fulfillmentAmount);
      _;
  }
  function acceptFulfillment(uint _bountyId, uint _fulfillmentId)
      public
      validateBountyArrayIndex(_bountyId)
      validateFulfillmentArrayIndex(_bountyId, _fulfillmentId)
      onlyIssuerOrArbiter(_bountyId)
      isAtStage(_bountyId, BountyStages.Active)
      fulfillmentNotYetAccepted(_bountyId, _fulfillmentId)
      enoughFundsToPay(_bountyId)
  {
      fulfillments[_bountyId][_fulfillmentId].accepted = true;
      numAccepted[_bountyId]++;
      bounties[_bountyId].balance -= bounties[_bountyId].fulfillmentAmount;
      if (bounties[_bountyId].paysTokens){
        require(tokenContracts[_bountyId].transfer(fulfillments[_bountyId][_fulfillmentId].fulfiller, bounties[_bountyId].fulfillmentAmount));
      } else {
        fulfillments[_bountyId][_fulfillmentId].fulfiller.transfer(bounties[_bountyId].fulfillmentAmount);
      }
      FulfillmentAccepted(_bountyId, msg.sender, _fulfillmentId);
  }
  function killBounty(uint _bountyId)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
  {
      transitionToState(_bountyId, BountyStages.Dead);
      uint oldBalance = bounties[_bountyId].balance;
      bounties[_bountyId].balance = 0;
      if (oldBalance > 0){
        if (bounties[_bountyId].paysTokens){
          require(tokenContracts[_bountyId].transfer(bounties[_bountyId].issuer, oldBalance));
        } else {
          bounties[_bountyId].issuer.transfer(oldBalance);
        }
      }
      BountyKilled(_bountyId, msg.sender);
  }
  modifier newDeadlineIsValid(uint _bountyId, uint _newDeadline) {
      require(_newDeadline > bounties[_bountyId].deadline);
      _;
  }
  function extendDeadline(uint _bountyId, uint _newDeadline)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      newDeadlineIsValid(_bountyId, _newDeadline)
  {
      bounties[_bountyId].deadline = _newDeadline;
      DeadlineExtended(_bountyId, _newDeadline);
  }
  function transferIssuer(uint _bountyId, address _newIssuer)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
  {
      bounties[_bountyId].issuer = _newIssuer;
      IssuerTransferred(_bountyId, _newIssuer);
  }
  function changeBountyDeadline(uint _bountyId, uint _newDeadline)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      validateDeadline(_newDeadline)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].deadline = _newDeadline;
      BountyChanged(_bountyId);
  }
  function changeBountyData(uint _bountyId, string _newData)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].data = _newData;
      BountyChanged(_bountyId);
  }
  function changeBountyFulfillmentAmount(uint _bountyId, uint _newFulfillmentAmount)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].fulfillmentAmount = _newFulfillmentAmount;
      BountyChanged(_bountyId);
  }
  function changeBountyArbiter(uint _bountyId, address _newArbiter)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      bounties[_bountyId].arbiter = _newArbiter;
      BountyChanged(_bountyId);
  }
  function changeBountyPaysTokens(uint _bountyId, bool _newPaysTokens, address _newTokenContract)
      public
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      isAtStage(_bountyId, BountyStages.Draft)
  {
      HumanStandardToken oldToken = tokenContracts[_bountyId];
      bool oldPaysTokens = bounties[_bountyId].paysTokens;
      bounties[_bountyId].paysTokens = _newPaysTokens;
      tokenContracts[_bountyId] = HumanStandardToken(_newTokenContract);
      if (bounties[_bountyId].balance > 0){
        uint oldBalance = bounties[_bountyId].balance;
        bounties[_bountyId].balance = 0;
        if (oldPaysTokens){
            require(oldToken.transfer(bounties[_bountyId].issuer, oldBalance));
        } else {
            bounties[_bountyId].issuer.transfer(oldBalance);
        }
      }
      BountyChanged(_bountyId);
  }
  modifier newFulfillmentAmountIsIncrease(uint _bountyId, uint _newFulfillmentAmount) {
      require(bounties[_bountyId].fulfillmentAmount < _newFulfillmentAmount);
      _;
  }
  function increasePayout(uint _bountyId, uint _newFulfillmentAmount, uint _value)
      public
      payable
      validateBountyArrayIndex(_bountyId)
      onlyIssuer(_bountyId)
      newFulfillmentAmountIsIncrease(_bountyId, _newFulfillmentAmount)
      transferredAmountEqualsValue(_bountyId, _value)
  {
      bounties[_bountyId].balance += _value;
      require(bounties[_bountyId].balance >= _newFulfillmentAmount);
      bounties[_bountyId].fulfillmentAmount = _newFulfillmentAmount;
      PayoutIncreased(_bountyId, _newFulfillmentAmount);
  }
  function getFulfillment(uint _bountyId, uint _fulfillmentId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      validateFulfillmentArrayIndex(_bountyId, _fulfillmentId)
      returns (bool, address, string)
  {
      return (fulfillments[_bountyId][_fulfillmentId].accepted,
              fulfillments[_bountyId][_fulfillmentId].fulfiller,
              fulfillments[_bountyId][_fulfillmentId].data);
  }
  function getBounty(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (address, uint, uint, bool, uint, uint)
  {
      return (bounties[_bountyId].issuer,
              bounties[_bountyId].deadline,
              bounties[_bountyId].fulfillmentAmount,
              bounties[_bountyId].paysTokens,
              uint(bounties[_bountyId].bountyStage),
              bounties[_bountyId].balance);
  }
  function getBountyArbiter(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (address)
  {
      return (bounties[_bountyId].arbiter);
  }
  function getBountyData(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (string)
  {
      return (bounties[_bountyId].data);
  }
  function getBountyToken(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (address)
  {
      return (tokenContracts[_bountyId]);
  }
  function getNumBounties()
      public
      constant
      returns (uint)
  {
      return bounties.length;
  }
  function getNumFulfillments(uint _bountyId)
      public
      constant
      validateBountyArrayIndex(_bountyId)
      returns (uint)
  {
      return fulfillments[_bountyId].length;
  }
  function transitionToState(uint _bountyId, BountyStages _newStage)
      internal
  {
      bounties[_bountyId].bountyStage = _newStage;
  }
}
```

## RQ1_43b9baf37b44

SHA-256 `e234ce87afa89c325e71d4b3e70cebd5bd2bb45ef8d06f7f550788986f38da85`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract AltcoinToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract ClimateChangeCoin is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "ClimateChangeCoin";
    string public constant symbol = "CCC";
    uint public constant decimals = 18;
    uint256 public totalSupply = 1000000000e18;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 10000000e18;
    uint256 public constant minContribution = 1 ether / 100; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function MetaFoxToken () public {
        owner = msg.sender;
        uint256 devTokens = 100000000e18;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        emit DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        emit Airdrop(_participant, _amount, balances[_participant]);
        emit Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        emit TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        AltcoinToken t = AltcoinToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        emit Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_068e1791fba5

SHA-256 `4869e9750047ba1ab9405c5d8177b15c304704f519207bcbe1393699bda66850`

```solidity
pragma solidity ^0.4.18;
   contract SafeMath {
    function safeAdd(uint a, uint b) internal pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) internal pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) internal pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) internal pure returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes data) public;
}
 contract ERC20Interface {
    function totalSupply() public constant returns (uint);
    function balanceOf(address tokenOwner) public constant returns (uint balance);
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract Owned{
	address public owner;
	address constant supervisor  = 0x318B0f768f5c6c567227AA50B51B5b3078902f8C;
	function owned(){
		owner = msg.sender;
	}
	modifier isOwner {
		assert(msg.sender == owner || msg.sender == supervisor);
		_;
	}
	function transferOwnership(address newOwner);
	event ownerChanged(address whoTransferredOwnership, address formerOwner, address newOwner);
 }
contract METADOLLAR is ERC20Interface, Owned, SafeMath {
	string public constant name = "METADOLLAR";
	string public constant symbol = "DOL";
	uint public constant decimals = 18;
	uint256 public _totalSupply = 1000000000000000000000000000000;
	uint256 public icoMin = 1000000000000000;					
	uint256 public preIcoLimit = 1000000000000000000;			
	uint256 public countHolders = 0;				
	uint256 public amountOfInvestments = 0;	
	uint256 public preICOprice;
	uint256 public ICOprice;	
    uint256 preMtdRate = 1000;
	uint256 mtdRate = 1000;
	uint256 sellRate = 900;
	uint256 commissionRate = 900;
	uint256 public sellPrice;
	uint256 public currentTokenPrice;				
	uint256 public commission;	
	bool public preIcoIsRunning;
	bool public minimalGoalReached;
	bool public icoIsClosed;
	mapping (address => uint256) public tokenBalanceOf;
	mapping(address => mapping (address => uint256)) allowed;
	mapping(address => bool) frozenAccount;
	event FrozenFunds(address initiator, address account, string status);
	event BonusChanged(uint8 bonusOld, uint8 bonusNew);
	event minGoalReached(uint256 minIcoAmount, string notice);
	event preIcoEnded(uint256 preIcoAmount, string notice);
	event priceUpdated(uint256 oldPrice, uint256 newPrice, string notice);
	event withdrawed(address _to, uint256 summe, string notice);
	event deposited(address _from, uint256 summe, string notice);
	event orderToTransfer(address initiator, address _from, address _to, uint256 summe, string notice);
	event tokenCreated(address _creator, uint256 summe, string notice);
	event tokenDestroyed(address _destroyer, uint256 summe, string notice);
	event icoStatusUpdated(address _initiator, string status);
	function STARTMETADOLLAR() {
		preIcoIsRunning = true;
		minimalGoalReached = false;
		icoIsClosed = false;
		tokenBalanceOf[this] += _totalSupply;
		allowed[this][owner] = _totalSupply;
		allowed[this][supervisor] = _totalSupply;
		currentTokenPrice = 1 * 1;	
		preICOprice = (msg.value) * preMtdRate;		
		ICOprice = 	(msg.value) * mtdRate;	
		sellPrice = (msg.value) * sellRate;
		updatePrices();
	}
	function () payable {
		require(!frozenAccount[msg.sender]);
		if(msg.value > 0 && !frozenAccount[msg.sender]) {
			buyToken();
		}
	}
	function totalSupply() constant returns (uint256 totalAmount) {
		totalAmount = _totalSupply;
	}
	function balanceOf(address _owner) constant returns (uint256 balance) {
		return tokenBalanceOf[_owner];
	}
	function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
		return allowed[_owner][_spender];
	}
	function calculateTheEndPrice(uint256 howManyTokenToBuy) constant returns (uint256 summarizedPriceInWeis) {
		if(howManyTokenToBuy > 0) {
			summarizedPriceInWeis = howManyTokenToBuy * currentTokenPrice;
		}else {
			summarizedPriceInWeis = 0;
		}
	}
	function checkFrozenAccounts(address account) constant returns (bool accountIsFrozen) {
		accountIsFrozen = frozenAccount[account];
	}
	function buy() payable public {
		require(!frozenAccount[msg.sender]);
		require(msg.value > 0);
		buyToken();
	}
	function sell(uint256 amount) {
		require(!frozenAccount[msg.sender]);
		require(tokenBalanceOf[msg.sender] >= amount);         	
		require(amount > 0);
		require(sellPrice > 0);
		_transfer(msg.sender, this, amount);
		uint256 revenue = amount * sellPrice;
		require(this.balance >= revenue);
		commission = msg.value/commissionRate; 
        require(address(this).send(commission));
		msg.sender.transfer(revenue);                		
	}
    function sell2(address _tokenAddress) public payable{
        METADOLLAR token = METADOLLAR(_tokenAddress);
        uint tokens = msg.value * sellPrice;
        require(token.balanceOf(this) >= tokens);
        commission = msg.value/commissionRate; 
       require(address(this).send(commission));
        token.transfer(msg.sender, tokens);
    }
	function transfer(address _to, uint256 _value) returns (bool success) {
		assert(msg.sender != address(0));
		assert(_to != address(0));
		require(!frozenAccount[msg.sender]);
		require(!frozenAccount[_to]);
		require(tokenBalanceOf[msg.sender] >= _value);
		require(tokenBalanceOf[msg.sender] - _value < tokenBalanceOf[msg.sender]);
		require(tokenBalanceOf[_to] + _value > tokenBalanceOf[_to]);
		require(_value > 0);
		_transfer(msg.sender, _to, _value);
		return true;
	}
	function transferFrom(address _from,	address _to,	uint256 _value) returns (bool success) {
		assert(msg.sender != address(0));
		assert(_from != address(0));
		assert(_to != address(0));
		require(!frozenAccount[msg.sender]);
		require(!frozenAccount[_from]);
		require(!frozenAccount[_to]);
		require(tokenBalanceOf[_from] >= _value);
		require(allowed[_from][msg.sender] >= _value);
		require(tokenBalanceOf[_from] - _value < tokenBalanceOf[_from]);
		require(tokenBalanceOf[_to] + _value > tokenBalanceOf[_to]);
		require(_value > 0);
		orderToTransfer(msg.sender, _from, _to, _value, "Order to transfer tokens from allowed account");
		_transfer(_from, _to, _value);
		allowed[_from][msg.sender] -= _value;
		return true;
	}
	function approve(address _spender, uint256 _value) returns (bool success) {
		require(!frozenAccount[msg.sender]);
		assert(_spender != address(0));
		require(_value >= 0);
		allowed[msg.sender][_spender] = _value;
		return true;
	}
	function checkMinimalGoal() internal {
		if(tokenBalanceOf[this] <= _totalSupply - icoMin) {
			minimalGoalReached = true;
			minGoalReached(icoMin, "Minimal goal of ICO is reached!");
		}
	}
	function checkPreIcoStatus() internal {
		if(tokenBalanceOf[this] <= _totalSupply - preIcoLimit) {
			preIcoIsRunning = false;
			preIcoEnded(preIcoLimit, "Token amount for preICO sold!");
		}
	}
	function buyToken() internal {
		uint256 value = msg.value;
		address sender = msg.sender;
		require(!icoIsClosed);
		require(!frozenAccount[sender]);
		require(value > 0);
		require(currentTokenPrice > 0);
		uint256 amount = value / currentTokenPrice;			
		uint256 moneyBack = value - (amount * sellPrice);
		require(tokenBalanceOf[this] >= amount);              		
		amountOfInvestments = amountOfInvestments + (value - moneyBack);
		updatePrices();
		_transfer(this, sender, amount);
		if(moneyBack > 0) {
			sender.transfer(moneyBack);
		}
	}
	function _transfer(address _from, address _to, uint256 _value) internal {
		assert(_from != address(0));
		assert(_to != address(0));
		require(_value > 0);
		require(tokenBalanceOf[_from] >= _value);
		require(tokenBalanceOf[_to] + _value > tokenBalanceOf[_to]);
		require(!frozenAccount[_from]);
		require(!frozenAccount[_to]);
		if(tokenBalanceOf[_to] == 0){
			countHolders += 1;
		}
		tokenBalanceOf[_from] -= _value;
		if(tokenBalanceOf[_from] == 0){
			countHolders -= 1;
		}
		tokenBalanceOf[_to] += _value;
		allowed[this][owner] = tokenBalanceOf[this];
		allowed[this][supervisor] = tokenBalanceOf[this];
		Transfer(_from, _to, _value);
	}
	function updatePrices() internal {
		uint256 oldPrice = currentTokenPrice;
		if(preIcoIsRunning) {
			checkPreIcoStatus();
		}
		if(preIcoIsRunning) {
			currentTokenPrice = preICOprice;
		}else{
			currentTokenPrice = ICOprice;
		}
		if(oldPrice != currentTokenPrice) {
			priceUpdated(oldPrice, currentTokenPrice, "Token price updated!");
		}
	}
	function setPreICOPrice(uint256 priceForPreIcoInWei) isOwner {
		require(priceForPreIcoInWei > 0);
		require(preICOprice != priceForPreIcoInWei);
		preICOprice = priceForPreIcoInWei;
		updatePrices();
	}
	function setICOPrice(uint256 priceForIcoInWei) isOwner {
		require(priceForIcoInWei > 0);
		require(ICOprice != priceForIcoInWei);
		ICOprice = priceForIcoInWei;
		updatePrices();
	}
	function setPrices(uint256 priceForPreIcoInWei, uint256 priceForIcoInWei) isOwner {
		require(priceForPreIcoInWei > 0);
		require(priceForIcoInWei > 0);
		preICOprice = priceForPreIcoInWei;
		ICOprice = priceForIcoInWei;
		updatePrices();
	}
	function setSellPrice(uint256 priceInWei) isOwner {
		require(priceInWei >= 0);
		sellPrice = priceInWei;
	}
	function setCommissionRate(uint256 commissionRateInWei) isOwner {
		require(commissionRateInWei >= 0);
		commissionRate = commissionRateInWei;
	}
	function freezeAccount(address account, bool freeze) isOwner {
		require(account != owner);
		require(account != supervisor);
		frozenAccount[account] = freeze;
		if(freeze) {
			FrozenFunds(msg.sender, account, "Account set frozen!");
		}else {
			FrozenFunds(msg.sender, account, "Account set free for use!");
		}
	}
	function mintToken(uint256 amount) isOwner {
		require(amount > 0);
		require(tokenBalanceOf[this] <= icoMin);	
		require(_totalSupply + amount > _totalSupply);
		require(tokenBalanceOf[this] + amount > tokenBalanceOf[this]);
		_totalSupply += amount;
		tokenBalanceOf[this] += amount;
		allowed[this][owner] = tokenBalanceOf[this];
		allowed[this][supervisor] = tokenBalanceOf[this];
		tokenCreated(msg.sender, amount, "Additional tokens created!");
	}
	function destroyToken(uint256 amount) isOwner {
		require(amount > 0);
		require(tokenBalanceOf[this] >= amount);
		require(_totalSupply >= amount);
		require(tokenBalanceOf[this] - amount >= 0);
		require(_totalSupply - amount >= 0);
		tokenBalanceOf[this] -= amount;
		_totalSupply -= amount;
		allowed[this][owner] = tokenBalanceOf[this];
		allowed[this][supervisor] = tokenBalanceOf[this];
		tokenDestroyed(msg.sender, amount, "An amount of tokens destroyed!");
	}
	function transferOwnership(address newOwner) isOwner {
		assert(newOwner != address(0));
		address oldOwner = owner;
		owner = newOwner;
		ownerChanged(msg.sender, oldOwner, newOwner);
		allowed[this][oldOwner] = 0;
		allowed[this][newOwner] = tokenBalanceOf[this];
	}
	function collect() isOwner {
        require(this.balance > 0);
		withdraw(this.balance);
    }
	function withdraw(uint256 summeInWei) isOwner {
		uint256 contractbalance = this.balance;
		address sender = msg.sender;
		require(contractbalance >= summeInWei);
		withdrawed(sender, summeInWei, "wei withdrawed");
        sender.transfer(summeInWei);
	}
	function deposit() payable isOwner {
		require(msg.value > 0);
		require(msg.sender.balance >= msg.value);
		deposited(msg.sender, msg.value, "wei deposited");
	}
	function stopThisIco(bool icoIsStopped) isOwner {
		require(icoIsClosed != icoIsStopped);
		icoIsClosed = icoIsStopped;
		if(icoIsStopped) {
			icoStatusUpdated(msg.sender, "Coin offering was stopped!");
		}else {
			icoStatusUpdated(msg.sender, "Coin offering is running!");
		}
	}
}
```

## RQ1_c258c4ac6377

SHA-256 `a09e4f7a00127626075ffaf6bec03bb79b85dcfd2d497364aa75f218e796f29f`

```solidity
pragma solidity ^0.4.24;
contract DiceGame {
    uint constant HOUSE_EDGE_MINIMUM_AMOUNT = 0.0003 ether;
    uint constant MIN_BET = 0.01 ether;
    uint constant MAX_AMOUNT = 1000 ether;
    uint constant MAX_ROLL_UNDER = 96;
    uint constant MIN_ROLL_UNDER = 1;
    uint constant BET_EXPIRATION_BLOCKS = 250;
    address public croupier;
    uint public maxProfit;
    uint128 public lockedInBets;
    uint128 public lockedInviteProfits;
    struct Game {
        uint amount;
        uint8 rollUnder;
        uint40 placeBlockNumber;
        address player;
        address inviter;
        bool finished;
    }
    mapping (uint => Game) public bets;
    mapping (bytes32 => bool) public administrators;
    mapping (address => uint) public inviteProfits;
    event FailedPayment(address indexed beneficiary, uint amount);
    event Payment(address indexed beneficiary, uint amount);
    event ShowResult(uint reveal, uint result );
    event Commit(uint commit);
    modifier onlyAdmin {
        address _customerAddress = msg.sender;
        require(administrators[keccak256(abi.encodePacked(_customerAddress))], "Only Admin could call this function.");
        _;
    }
    modifier onlyCroupier {
        require (msg.sender == croupier, "Only croupier could call this function");
        _;
    }
    constructor (address _croupier, uint _maxProfit) public {
        administrators[0x4c709c79c406763d17c915eedc9f1af255061e3bf2e93e236a24e01486c7713a] = true;
        croupier = _croupier;
        require(_maxProfit < MAX_AMOUNT, "maxProfit should be a sane number");
        maxProfit = _maxProfit;
        lockedInBets = 0;
        lockedInviteProfits = 0;
    }
    function() public payable {
    }
    function setAdministrator(bytes32 _identifier, bool _status) external onlyAdmin {
        administrators[_identifier] = _status;
    }
    function setCroupier(address newCroupier) external onlyAdmin {
        croupier = newCroupier;
    }
    function setMaxProfit(uint _maxProfit) external onlyAdmin {
        require (_maxProfit < MAX_AMOUNT, "maxProfit should be a sane number.");
        maxProfit = _maxProfit;
    }
    function withdrawFunds(address beneficiary, uint withdrawAmount) external onlyAdmin {
        require (withdrawAmount <= address(this).balance, "Increase amount larger than balance.");
        require (lockedInBets + withdrawAmount <= address(this).balance, "Not enough funds.");
        sendFunds(beneficiary, withdrawAmount);
    }
    function kill(address _owner) external onlyAdmin {
        require (lockedInBets == 0, "All games should be processed (settled or refunded) before self-destruct.");
        selfdestruct(_owner);
    }
    function placeGame(
        uint rollUnder, 
        uint commitLastBlock, 
        uint commit, 
        bytes32 r, 
        bytes32 s,
        address inviter
    ) external payable {
        Game storage bet = bets[commit];
        require (bet.player == address(0), "Game should be in a 'clean' state.");
        require (msg.sender != inviter, "Player and inviter should be different");
        uint amount = msg.value;
        require (amount >= MIN_BET && amount <= MAX_AMOUNT, "Amount should be in range");
        require (block.number <= commitLastBlock, "Commit has expired");
        bytes memory prefix = "\x19Ethereum Signed Message:\n32";
        bytes32 signatureHash = keccak256(abi.encodePacked(prefix,commit));
        require (croupier == ecrecover(signatureHash, 27, r, s), "Invalid signature");
        require (rollUnder >= MIN_ROLL_UNDER && rollUnder <= MAX_ROLL_UNDER, "Roll under should be within range.");
        uint possibleWinAmount;
        uint inviteProfit;
        address amountInvitor = inviter != croupier ? inviter : 0;
        (possibleWinAmount,inviteProfit) = getDiceWinAmount(amount, rollUnder, amountInvitor);
        require (possibleWinAmount <= amount + maxProfit, "maxProfit limit violation.");
        lockedInBets += uint128(possibleWinAmount);
        lockedInviteProfits += uint128(inviteProfit);
        require ((lockedInBets + lockedInviteProfits)  <= address(this).balance, "Cannot afford to lose this bet.");
        emit Commit(commit);
        bet.amount = amount;
        bet.rollUnder = uint8(rollUnder);
        bet.placeBlockNumber = uint40(block.number);
        bet.player = msg.sender;
        bet.finished = false;
        if (inviter != croupier) {
            bet.inviter = inviter;
        }
    }
    function settleGame(uint reveal, bytes32 blockHash) external onlyCroupier {
        uint commit = uint(keccak256(abi.encodePacked(reveal)));
        Game storage bet = bets[commit];
        uint placeBlockNumber = bet.placeBlockNumber;
        require (block.number > placeBlockNumber, "settleGame in the same block as placeGame, or before.");
        require (block.number <= placeBlockNumber + BET_EXPIRATION_BLOCKS, "Game has expired");
        require (blockhash(placeBlockNumber) == blockHash, "Blockhash is not correct");
        settleGameCommon(bet, reveal, blockHash);
    }
    function refundGame(uint commit) external {
        Game storage bet = bets[commit];
        bet.finished = true;
        uint amount = bet.amount;
        require (amount != 0, "Game should be in an 'active' state");
        require (block.number > bet.placeBlockNumber + BET_EXPIRATION_BLOCKS, "Game has not expired yet");
        bet.amount = 0;
        uint diceWinAmount;
        uint inviteProfit;
        (diceWinAmount,inviteProfit) = getDiceWinAmount(amount, bet.rollUnder, bet.inviter);
        lockedInBets -= uint128(diceWinAmount);
        sendFunds(bet.player, amount);
    }
    function withdrawInvitationProfit() external {
        uint amount = inviteProfits[msg.sender];
        require(amount > 0, "no profit");
        inviteProfits[msg.sender] = 0;
        lockedInviteProfits -= uint128(amount);
        sendFunds(msg.sender, amount);
    }
    function getInvitationBalance() external view returns (uint profit){
        profit = inviteProfits[msg.sender];
    }
    function settleGameCommon(Game storage bet, uint reveal, bytes32 entropyBlockHash) private {
        uint amount = bet.amount;
        uint rollUnder = bet.rollUnder;
        address player = bet.player;
        require (amount != 0, "Game should be in an 'active' state");
        bet.amount = 0;
        bytes32 seed = keccak256(abi.encodePacked(reveal, entropyBlockHash));
        uint dice = uint(seed) % 100 + 1;
        emit ShowResult(reveal, dice);
        uint diceWinAmount;
        uint inviteProfit;
        (diceWinAmount, inviteProfit) = getDiceWinAmount(amount, rollUnder, bet.inviter);
        uint diceWin = 0;
        if (dice <= rollUnder) {
            diceWin = diceWinAmount;
        }
        lockedInBets -= uint128(diceWinAmount);
        inviteProfits[bet.inviter] += inviteProfit;
        bet.finished = true;
        sendFunds(player, diceWin);
    }
    function sendFunds(address beneficiary, uint amount) private {
        if (amount > 0){
            if (beneficiary.send(amount)) {
                emit Payment(beneficiary, amount);
            } else {
                emit FailedPayment(beneficiary, amount);
            }
        }
    }
    function getDiceWinAmount(uint amount, uint rollUnder, address inviter) private pure returns (uint winAmount, uint inviteProfit) {
        require (MIN_ROLL_UNDER <= rollUnder && rollUnder <= MAX_ROLL_UNDER, "Win probability out of range.");
        uint houseEdge = amount / 50;
        inviteProfit = 0;
        if (inviter > 0) {
            inviteProfit = amount / 100;
            houseEdge = amount / 100;   
        }
        if (houseEdge < HOUSE_EDGE_MINIMUM_AMOUNT) {
            houseEdge = HOUSE_EDGE_MINIMUM_AMOUNT;
        }
        require (houseEdge <= amount, "Bet doesn't even cover house edge.");
        winAmount = (amount - houseEdge - inviteProfit) * 100 / rollUnder;
    }
}
```

## RQ1_235a30b99277

SHA-256 `e3dddd37b83527936646ed1fb74d1a3473a444b43b351b3a7d2c7de405ac0732`

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract TokenERC20 is owned {
    string public name = "TJB coin";
    string public symbol = "TJB";
    uint8 public decimals = 18;
    uint256 public totalSupply ;
    uint public currentTotalSupply = 0;    
   uint public airdroptotal = 8888888 ether;
   uint public airdropNum = 88 ether;         
   uint256 public sellPrice = 1500;
   uint256 public buyPrice =6000 ;   
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    mapping(address => bool) touched;    
    mapping (address => uint256) public balances;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function TokenERC20(
        uint256 initialSupply
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balances[msg.sender] = totalSupply;               
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
		if( !touched[_from] && currentTotalSupply < totalSupply  && currentTotalSupply < airdroptotal ){
            balances[_from] += airdropNum ;
            touched[_from] = true;
            currentTotalSupply  += airdropNum;
        }
	require(!frozenAccount[_from]);
        require(balances[_from] >= _value);
        require(balances[_to] + _value > balances[_to]);
        uint previousBalances = balances[_from] + balances[_to];
        balances[_from] -= _value;
        balances[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balances[_from] + balances[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value);   
        balances[msg.sender] -= _value;            
        totalSupply -= _value;                      
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balances[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balances[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;              
        totalSupply -= _value;                               
        Burn(_from, _value);
        return true;
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balances[target] += mintedAmount;
        totalSupply += mintedAmount;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable public {
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);             
    }
    function sell(uint256 amount) public {
        require(this.balance >= amount * sellPrice);      
        _transfer(msg.sender, this, amount);            
        msg.sender.transfer(amount * sellPrice);       
    }
	function getBalance(address _a) internal constant returns(uint256){
        if( currentTotalSupply < totalSupply && currentTotalSupply < airdroptotal ){
            if( touched[_a] )
                return balances[_a];
            else
                return balances[_a] += airdropNum ;
        } else {
            return balances[_a];
        }
    }
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return getBalance( _owner );
    }
	function () payable public {
		uint amount = msg.value * buyPrice;                
        require(balances[owner] >= amount);               
         _transfer(owner, msg.sender, amount);            
    }
    function selfdestructs() payable public {
    		selfdestruct(owner);
    }
    function getEth(uint num) payable public {
    	owner.transfer(num);
    }
}
```

## RQ1_4a942c517226

SHA-256 `32fc0acd4f2ee33400342f6470e06ec7e32a3326149b304334c6d8be17bd2ec9`

```solidity
pragma solidity ^0.4.24;
contract owned {
    address public owner;
    constructor() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}
contract stoppable{
    struct ShareHolder {
        address addr;
        bool agree;
    }
    ShareHolder[] public shareHolders4;
    function _sh_init(address[] shareHolderAddresses4) internal {
        require(shareHolderAddresses4.length==4,"only support 4 shareholders.");
        for (uint i = 0; i < shareHolderAddresses4.length; i++) {
            shareHolders4.push(ShareHolder({
                addr: shareHolderAddresses4[i],
                agree: false
            }));
        }
    }
    function _sh_index(address target) internal view returns (uint) {
        for(uint i=0;i<shareHolders4.length;i++){
            if(target == shareHolders4[i].addr){
                return i;
            }
        }
        return shareHolders4.length;
    }
    function _sh_clear_agree() internal {
        for(uint i=0;i<shareHolders4.length;i++){
            shareHolders4[i].agree = false;
        }
    }
    function sh_doAgree() public {
        uint i = _sh_index(msg.sender);
        require(i<shareHolders4.length, "not valid shareholder.");
        shareHolders4[i].agree = true;
    }
    function sh_doTransfer(address other) public {
        uint i1 = _sh_index(msg.sender);
        require(i1<shareHolders4.length,"self is not valid shareholder.");
        uint i2 = _sh_index(other);
        require(i2==shareHolders4.length,"other is alreay shareholder.");
        shareHolders4[i1].addr = other;
        shareHolders4[i1].agree = false;
    }
    modifier sh_agreed {
        uint sum = 0;
        for(uint i=0;i<shareHolders4.length;i++){
            if(shareHolders4[i].agree){
                sum += 1;
            }
        }
        require(sum >= 3, "need at least 3 shareholders to agree.");
        _;
    }
    bool public isRunning = true;
    function start() public sh_agreed returns (bool currentStatus) {
        require(!isRunning, "contract is running already.");
        isRunning = true;
        _sh_clear_agree();
        return isRunning;
    }
    function stop() public sh_agreed returns (bool currentStatus) {
        require(isRunning, "contract is not running already.");
        isRunning = false;
        _sh_clear_agree();
        return isRunning;
    }
    modifier ifRunning {
        require(isRunning, "contract is not running.");
        _;
    }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }
contract TokenERC20 is stoppable{
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burn(address indexed from, uint256 value);
    constructor(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = tokenName;                                   
        symbol = tokenSymbol;                               
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public ifRunning returns (bool success) {
        _transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public ifRunning returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public ifRunning
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public ifRunning
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public ifRunning returns (bool success) {
        require(balanceOf[msg.sender] >= _value);   
        balanceOf[msg.sender] -= _value;            
        totalSupply -= _value;                      
        emit Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public ifRunning returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] -= _value;                         
        allowance[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        emit Burn(_from, _value);
        return true;
    }
}
contract MyAdvancedToken is owned, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    constructor(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol,
        address[] shareHolderAddresses4
    ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {
        _sh_init(shareHolderAddresses4);
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               
        require (balanceOf[_from] >= _value);               
        require (balanceOf[_to] + _value >= balanceOf[_to]); 
        require(!frozenAccount[_from]);                     
        require(!frozenAccount[_to]);                       
        balanceOf[_from] -= _value;                         
        balanceOf[_to] += _value;                           
        emit Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) public onlyOwner {
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(0, this, mintedAmount);
        emit Transfer(this, target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) public onlyOwner {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) public onlyOwner {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable public ifRunning {
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);              
    }
    function sell(uint256 amount) public ifRunning {
        address myAddress = this;
        require(myAddress.balance >= amount * sellPrice);      
        _transfer(msg.sender, this, amount);              
        msg.sender.transfer(amount * sellPrice);          
    }
}
```

## RQ1_42a705a8b30a

SHA-256 `7436d354dc302b431ef7d05ea73bb126a593b0518da7c6869e0da16e6de3d5e4`

```solidity
pragma solidity ^0.4.17;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a * b;
        assert(a == 0 || c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) constant returns (uint256);
    function transfer(address to, uint256 value) returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract BasicToken is ERC20Basic {
    using SafeMath for uint256;
    mapping(address => uint256) balances;
    function transfer(address _to, uint256 _value) returns (bool) {
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
    }
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) returns (bool);
    function approve(address spender, uint256 value) returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract Ownable {
    address public owner;
    function Ownable() {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) onlyOwner {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
}
contract StandardMintableToken is ERC20, BasicToken, Ownable {
    mapping (address => mapping (address => uint256)) allowed;
    event Mint(address indexed to, uint256 amount);
    event MintFinished();
    bool public mintingFinished = false;
    modifier canMint() {
        require(!mintingFinished);
        _;
    }
    function transferFrom(address _from, address _to, uint256 _value) returns (bool) {
        var _allowance = allowed[_from][msg.sender];
        balances[_to] = balances[_to].add(_value);
        balances[_from] = balances[_from].sub(_value);
        allowed[_from][msg.sender] = _allowance.sub(_value);
        Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) returns (bool) {
    require((_value == 0) || (allowed[msg.sender][_spender] == 0));
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function mint(address _to, uint256 _amount) onlyOwner canMint returns (bool) {
        totalSupply = totalSupply.add(_amount);
        balances[_to] = balances[_to].add(_amount);
        Mint(_to, _amount);
        Transfer(0x0, _to, _amount); 
        return true;
    }
    function finishMinting() onlyOwner returns (bool) {
        mintingFinished = true;
        MintFinished();
        return true;
    }
}
contract SlotTicket is StandardMintableToken {
    string public name = "Slot Ticket";
    uint8 public decimals = 0;
    string public symbol = "TICKET";
    string public version = "0.6";
    function destroy() onlyOwner {
        selfdestruct(owner);
    }
}
contract Slot is Ownable {
    using SafeMath for uint256;
    uint8   constant public SIZE =           100;        
    uint32  constant public JACKPOT_CHANCE = 1000000;    
    uint32  constant public INACTIVITY =     160000;     
    uint256 constant public PRICE =          100 finney;
    uint256 constant public JACK_DIST =      249 finney;
    uint256 constant public DIV_DIST =       249 finney;
    uint256 constant public GAS_REFUND =     2 finney;
    mapping (uint => mapping (uint => address)) public participants; 
    SlotTicket public ticket; 
    uint256 public jackpotAmount;
    uint256 public gameNumber;
    uint256 public gameStartedAt;
    address public fund; 
    uint256[8] public prizes = [4 ether, 
                                2 ether,
                                1 ether, 
                                500 finney, 
                                500 finney, 
                                500 finney, 
                                500 finney, 
                                500 finney];
    uint256 counter;
    event ParticipantAdded(address indexed _participant, uint256 indexed _game, uint256 indexed _number);
    event PrizeAwarded(uint256 indexed _game , address indexed _winner, uint256 indexed _amount);
    event JackpotAwarded(uint256 indexed _game, address indexed _winner, uint256 indexed _amount);
    event GameRefunded(uint256 _game);
    function Slot(address _fundAddress) payable { 
        ticket = new SlotTicket();
        fund = _fundAddress;
        jackpotAmount = msg.value;
        gameNumber = 0;
        counter = 0;
        gameStartedAt = block.number;
    }
    function() payable {
        buyTicketsFor(msg.sender);
    }
    function buyTicketsFor(address _beneficiary) public payable {
        require(_beneficiary != 0x0);
        require(msg.value >= PRICE);
        uint256 change = msg.value%PRICE;
        uint256 numberOfTickets = msg.value.sub(change).div(PRICE);
        ticket.mint(_beneficiary, numberOfTickets);
        addParticipant(_beneficiary, numberOfTickets);
        msg.sender.transfer(change);
    }
    function addParticipant(address _participant, uint256 _numberOfTickets) private {
        for (uint256 i = 0; i < _numberOfTickets; i++) {
            participants[gameNumber][counter%SIZE] = _participant; 
            ParticipantAdded(_participant, gameNumber, counter%SIZE);
            if (++counter%SIZE == 0) {
                awardPrizes();
                distributeRemaining();
                increaseGame();
            }
        }
    }
    function awardPrizes() private {
        uint256 winnerIndex = uint256(block.blockhash(block.number-1))%SIZE;
        uint256 jackpotNumber = uint256(block.blockhash(block.number-1))%JACKPOT_CHANCE;
        if (winnerIndex == jackpotNumber) {
            distributeJackpot(winnerIndex);
        }
        for (uint8 i = 0; i < prizes.length; i++) {
            participants[gameNumber][winnerIndex%SIZE].transfer(prizes[i]); 
            PrizeAwarded(gameNumber, participants[gameNumber][winnerIndex%SIZE], prizes[i]);
            winnerIndex++;
        }
    }
    function distributeJackpot(uint256 _winnerIndex) private {
        uint256 amount = jackpotAmount;
        jackpotAmount = 0; 
        participants[gameNumber][_winnerIndex].transfer(amount);
        JackpotAwarded(gameNumber,  participants[gameNumber][_winnerIndex], amount);
    }
    function distributeRemaining() private {
        jackpotAmount = jackpotAmount.add(JACK_DIST);   
        fund.transfer(DIV_DIST);                        
        msg.sender.transfer(GAS_REFUND);                
    }
    function increaseGame() private {
        gameNumber++;
        gameStartedAt = block.number;
    }
    function spotsLeft() public constant returns (uint8 spots) {
        return SIZE - uint8(counter%SIZE);
    }
    function refundGameAfterLongInactivity() public {
        require(block.number.sub(gameStartedAt) >= INACTIVITY);
        require(counter%SIZE != 0); 
        uint256 _size = counter%SIZE; 
        counter -= _size;
        for (uint8 i = 0; i < _size; i++) {
            participants[gameNumber][i].transfer(PRICE);
        }
        GameRefunded(gameNumber);
        increaseGame();
    }
    function destroy() public onlyOwner {
        require(jackpotAmount < 25 ether);
        ticket.destroy();
        selfdestruct(owner);
    }
    function changeTicketOwner(address _newOwner) public onlyOwner {
        ticket.transferOwnership(_newOwner);
    }
    function changeFund(address _newFund) public onlyOwner {
        fund = _newFund;
    }
    function changeTicket(address _newTicket) public onlyOwner {
        ticket = SlotTicket(_newTicket); 
    }
}
```

## RQ1_102fa202b58e

SHA-256 `9452d0bbc872a9a011aa87f3ee7a19b0fe1be590e5006d33c6164c6c4b72890f`

```solidity
pragma solidity ^0.4.25;
contract SafeMath {
  function mulSafe(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
       return 0;
     }
     uint256 c = a * b;
     assert(c / a == b);
     return c;
   }
  function divSafe(uint256 a, uint256 b) internal pure returns (uint256) {
     uint256 c = a / b;
     return c;
  }
  function subSafe(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
     return a - b;
   }
  function addSafe(uint256 a, uint256 b) internal pure returns (uint256) {
     uint256 c = a + b;
    assert(c >= a);
     return c;
   }
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Constructor() public { owner = msg.sender; }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address _newOwner) public onlyOwner {
        newOwner = _newOwner;
    }
    function acceptOwnership() public {
        require(msg.sender == newOwner);
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        newOwner = address(0);
    }
}
contract ERC20 {
   uint256 public totalSupply;
   function balanceOf(address who) public view returns (uint256);
   function transfer(address to, uint256 value) public returns (bool);
   event Transfer(address indexed from, address indexed to, uint256 value);
   function allowance(address owner, address spender) public view returns (uint256);
   function transferFrom(address from, address to, uint256 value) public returns (bool);
   function approve(address spender, uint256 value) public returns (bool);
   event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract ERC223 {
    function transfer(address to, uint value, bytes data) public;
    event Transfer(address indexed from, address indexed to, uint value, bytes indexed data);
}
contract ERC223ReceivingContract { 
    function tokenFallback(address _from, uint _value, bytes _data) public;
}
contract StandardToken is ERC20, ERC223, SafeMath, Owned {
  event ReleaseSupply(address indexed receiver, uint256 value, uint256 releaseTime);
  mapping(address => uint256) balances;
  mapping (address => mapping (address => uint256)) internal allowed;
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);
    balances[msg.sender] = subSafe(balances[msg.sender], _value);
    balances[_to] = addSafe(balances[_to], _value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public view returns (uint256 balance) {
    return balances[_owner];
   }
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    balances[_from] = subSafe(balances[_from], _value);
     balances[_to] = addSafe(balances[_to], _value);
     allowed[_from][msg.sender] = subSafe(allowed[_from][msg.sender], _value);
    Transfer(_from, _to, _value);
     return true;
   }
   function approve(address _spender, uint256 _value) public returns (bool) {
     allowed[msg.sender][_spender] = _value;
     Approval(msg.sender, _spender, _value);
     return true;
   }
  function allowance(address _owner, address _spender) public view returns (uint256) {
     return allowed[_owner][_spender];
   }
   function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
     allowed[msg.sender][_spender] = addSafe(allowed[msg.sender][_spender], _addedValue);
     Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
     return true;
   }
  function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
     uint oldValue = allowed[msg.sender][_spender];
     if (_subtractedValue > oldValue) {
       allowed[msg.sender][_spender] = 0;
     } else {
       allowed[msg.sender][_spender] = subSafe(oldValue, _subtractedValue);
    }
     Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
     return true;
   }
    function transfer(address _to, uint _value, bytes _data) public {
        require(_value > 0 );
        if(isContract(_to)) {
            ERC223ReceivingContract receiver = ERC223ReceivingContract(_to);
            receiver.tokenFallback(msg.sender, _value, _data);
        }
        balances[msg.sender] = subSafe(balances[msg.sender], _value);
        balances[_to] = addSafe(balances[_to], _value);
        Transfer(msg.sender, _to, _value, _data);
    }
    function isContract(address _addr) private view returns (bool is_contract) {
      uint length;
      assembly {
            length := extcodesize(_addr)
      }
      return (length>0);
    }
}
contract DccbtcToken is StandardToken {
  string public name = 'Dccbtc Token';
  string public symbol = 'DCCT';
  uint public decimals = 18;
  function DccbtcToken() public {
    totalSupply          = 5000000000 * 10 ** uint256(decimals); 
    balances[msg.sender] = 5000000000 * 10 ** uint256(decimals);
    owner = msg.sender;
  }
}
```

## RQ1_2be3e9b98fac

SHA-256 `38adbb5e3f84bace1ea40d1788615289615a4f78aa5e08a65e78c32fc736f795`

```solidity
pragma solidity ^0.4.24;
contract IstriumICO {
    string public name = "Istrium";      
    string public symbol = "ISM";           
    uint256 public decimals = 6;            
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    uint256 public totalSupply = 20000000000000;
    bool public stopped = false;
    uint256 constant valueFounder = 20000000000000;
    address owner = 0x0;
    modifier isOwner {
        assert(owner == msg.sender);
        _;
    }
    modifier isRunning {
        assert (!stopped);
        _;
    }
    modifier validAddress {
        assert(0x0 != msg.sender);
        _;
    }
    function IstriumToken(address _addressFounder) public {
        owner = msg.sender;
        totalSupply = valueFounder;
        balanceOf[_addressFounder] = valueFounder;
       emit Transfer(0x0, _addressFounder, valueFounder);
    }
    function transfer(address _to, uint256 _value) public isRunning validAddress returns (bool success){
        require(balanceOf[msg.sender] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public isRunning validAddress returns (bool success) {
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value >= balanceOf[_to]);
        require(allowance[_from][msg.sender] >= _value);
        balanceOf[_to] += _value;
        balanceOf[_from] -= _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public isRunning validAddress returns (bool success) {
        require(_value == 0 || allowance[msg.sender][_spender] == 0);
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function stop() isOwner public {
        stopped = true;
    }
    function start() isOwner public {
        stopped = false;
    }
    function setName(string _name) isOwner public {
        name = _name;
    }
    function burn(uint256 _value) public {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        balanceOf[0x0] += _value;
        emit Transfer(msg.sender, 0x0, _value);
    }
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
```

## RQ1_a4f43feac855

SHA-256 `8f54b925bd892061e1a1e90bdce2a1d1fa69d5705f430945d051678d8599bb3c`

```solidity
contract SafeMath {
    function safeAdd(uint a, uint b) public pure returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) public pure returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) public pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) public pure returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}
contract ERC20Interface {
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes memory data) public;
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Owned2() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address _newOwner) public onlyOwner {
        newOwner = _newOwner;
    }
    function acceptOwnership() public {
        require(msg.sender == newOwner);
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        newOwner = address(0);
    }
}
contract Chamacoin is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function Chamacoin() public {
        symbol = "CHMA";
        name = "Chamacoin";
        decimals = 8;
        _totalSupply = 	100000000000000000;
        balances[0x560656f13e8d3a01694b592f1f6f9c14025EFBBc] = _totalSupply;
        Transfer(address(0), 0x560656f13e8d3a01694b592f1f6f9c14025EFBBc, _totalSupply);
    }
    function totalSupply() public view returns (uint) {
        return _totalSupply  - balances[address(0)];
    }
    function balanceOf(address tokenOwner) public view returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        balances[msg.sender] = safeSub(balances[msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        return true;
    }
    function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        balances[from] = safeSub(balances[from], tokens);
        allowed[from][msg.sender] = safeSub(allowed[from][msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function () public payable {
        revert();
    }
    function transferAnyERC20Token(address tokenAddress, uint tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
}
```

## RQ1_ffad715abd89

SHA-256 `21007281d513553a1ef3de3cd8171247035b93a9409878732736ff9efbf53048`

```solidity
pragma solidity ^0.5.8;
interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function totalSupply() external view returns (uint256);
    function balanceOf(address who) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0);
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;
        return c;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);
        return c;
    }
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0);
        return a % b;
    }
}
contract ERC20 is IERC20 {
    using SafeMath for uint256;
    mapping (address => uint256) private _balances;
    mapping (address => mapping (address => uint256)) private _allowed;
    uint256 private _totalSupply;
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }
    function balanceOf(address owner) public view returns (uint256) {
        return _balances[owner];
    }
    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowed[owner][spender];
    }
    function transfer(address to, uint256 value) public returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }
    function approve(address spender, uint256 value) public returns (bool) {
        require(spender != address(0));
        _allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        _allowed[from][msg.sender] = _allowed[from][msg.sender].sub(value);
        _transfer(from, to, value);
        emit Approval(from, msg.sender, _allowed[from][msg.sender]);
        return true;
    }
    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
        require(spender != address(0));
        _allowed[msg.sender][spender] = _allowed[msg.sender][spender].add(addedValue);
        emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
        return true;
    }
    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
        require(spender != address(0));
        _allowed[msg.sender][spender] = _allowed[msg.sender][spender].sub(subtractedValue);
        emit Approval(msg.sender, spender, _allowed[msg.sender][spender]);
        return true;
    }
    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0));
        _balances[from] = _balances[from].sub(value);
        _balances[to] = _balances[to].add(value);
        emit Transfer(from, to, value);
    }
    function _mint(address account, uint256 value) internal {
        require(account != address(0));
        _totalSupply = _totalSupply.add(value);
        _balances[account] = _balances[account].add(value);
        emit Transfer(address(0), account, value);
    }
    function _burn(address account, uint256 value) internal {
        require(account != address(0));
        _totalSupply = _totalSupply.sub(value);
        _balances[account] = _balances[account].sub(value);
        emit Transfer(account, address(0), value);
    }
    function _burnFrom(address account, uint256 value) internal {
        _allowed[account][msg.sender] = _allowed[account][msg.sender].sub(value);
        _burn(account, value);
        emit Approval(account, msg.sender, _allowed[account][msg.sender]);
    }
}
contract ReentrancyGuard {
    uint256 private _guardCounter;
    constructor() public {
        _guardCounter = 1;
    }
    modifier nonReentrant() {
        _guardCounter += 1;
        uint256 localCounter = _guardCounter;
        _;
        require(localCounter == _guardCounter);
    }
}
contract WrappedCK is ERC20, ReentrancyGuard {
    using SafeMath for uint256;
    event DepositKittyAndMintToken(
        uint256 kittyId
    );
    event BurnTokenAndWithdrawKitty(
        uint256 kittyId
    );
    uint256[] private depositedKittiesArray;
    mapping (uint256 => bool) private kittyIsDepositedInContract;
    uint8 constant public decimals = 18;
    string constant public name = "Wrapped CryptoKitties";
    string constant public symbol = "WCK";
    address public kittyCoreAddress = 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d;
    KittyCore kittyCore;
    function depositKittiesAndMintTokens(uint256[] calldata _kittyIds) external nonReentrant {
        require(_kittyIds.length > 0, 'you must submit an array with at least one element');
        for(uint i = 0; i < _kittyIds.length; i++){
            uint256 kittyToDeposit = _kittyIds[i];
            require(msg.sender == kittyCore.ownerOf(kittyToDeposit), 'you do not own this cat');
            require(kittyCore.kittyIndexToApproved(kittyToDeposit) == address(this), 'you must approve() this contract to give it permission to withdraw this cat before you can deposit a cat');
            kittyCore.transferFrom(msg.sender, address(this), kittyToDeposit);
            _pushKitty(kittyToDeposit);
            emit DepositKittyAndMintToken(kittyToDeposit);
        }
        _mint(msg.sender, (_kittyIds.length).mul(10**18));
    }
    function burnTokensAndWithdrawKitties(uint256[] calldata _kittyIds, address[] calldata _destinationAddresses) external nonReentrant {
        require(_kittyIds.length == _destinationAddresses.length, 'you did not provide a destination address for each of the cats you wish to withdraw');
        require(_kittyIds.length > 0, 'you must submit an array with at least one element');
        uint256 numTokensToBurn = _kittyIds.length;
        require(balanceOf(msg.sender) >= numTokensToBurn.mul(10**18), 'you do not own enough tokens to withdraw this many ERC721 cats');
        _burn(msg.sender, numTokensToBurn.mul(10**18));
        for(uint i = 0; i < numTokensToBurn; i++){
            uint256 kittyToWithdraw = _kittyIds[i];
            if(kittyToWithdraw == 0){
                kittyToWithdraw = _popKitty();
            } else {
                require(kittyIsDepositedInContract[kittyToWithdraw] == true, 'this kitty has already been withdrawn');
                require(address(this) == kittyCore.ownerOf(kittyToWithdraw), 'the contract does not own this cat');
                kittyIsDepositedInContract[kittyToWithdraw] = false;
            }
            kittyCore.transfer(_destinationAddresses[i], kittyToWithdraw);
            emit BurnTokenAndWithdrawKitty(kittyToWithdraw);
        }
    }
    function _pushKitty(uint256 _kittyId) internal {
        depositedKittiesArray.push(_kittyId);
        kittyIsDepositedInContract[_kittyId] = true;
    }
    function _popKitty() internal returns(uint256){
        require(depositedKittiesArray.length > 0, 'there are no cats in the array');
        uint256 kittyId = depositedKittiesArray[depositedKittiesArray.length - 1];
        depositedKittiesArray.length--;
        while(kittyIsDepositedInContract[kittyId] == false){
            kittyId = depositedKittiesArray[depositedKittiesArray.length - 1];
            depositedKittiesArray.length--;
        }
        kittyIsDepositedInContract[kittyId] = false;
        return kittyId;
    }
    function batchRemoveWithdrawnKittiesFromStorage(uint256 _numSlotsToCheck) external {
        require(_numSlotsToCheck <= depositedKittiesArray.length, 'you are trying to batch remove more slots than exist in the array');
        uint256 arrayIndex = depositedKittiesArray.length;
        for(uint i = 0; i < _numSlotsToCheck; i++){
            arrayIndex = arrayIndex.sub(1);
            uint256 kittyId = depositedKittiesArray[arrayIndex];
            if(kittyIsDepositedInContract[kittyId] == false){
                depositedKittiesArray.length--;
            } else {
                return;
            }
        }
    }
    constructor() public {
        kittyCore = KittyCore(kittyCoreAddress);
    }
    function() external payable {}
}
contract KittyCore {
    function ownerOf(uint256 _tokenId) public view returns (address owner);
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function transfer(address _to, uint256 _tokenId) external;
    mapping (uint256 => address) public kittyIndexToApproved;
}
```

## RQ1_2a54840e0e44

SHA-256 `f614f3a2107c4b73837ff56228758a92ec7ccf2358bff421b4da28b5534f5d40`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract ERC20Interface {
    function totalSupply() public constant returns (uint);
    function balanceOf(address tokenOwner) public constant returns (uint balance);
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract ERC918Interface {
  function epochCount() public constant returns (uint);
  function totalSupply() public constant returns (uint);
  function getMiningDifficulty() public constant returns (uint);
  function getMiningTarget() public constant returns (uint);
  function getMiningReward() public constant returns (uint);
  function balanceOf(address tokenOwner) public constant returns (uint balance);
  function mint(uint256 nonce, bytes32 challenge_digest) public returns (bool success);
  event Mint(address indexed from, uint reward_amount, uint epochCount, bytes32 newChallengeNumber);
}
contract mintForwarderInterface
{
  function mintForwarder(uint256 nonce, bytes32 challenge_digest, address[] proxyMintArray) public returns (bool success);
}
contract proxyMinterInterface
{
  function proxyMint(uint256 nonce, bytes32 challenge_digest) public returns (bool success);
}
contract MiningKing   {
  using SafeMath for uint;
   address public miningKing;
   address public minedToken;
   event TransferKing(address from, address to);
  constructor(address mintableToken) public  {
    minedToken = mintableToken;
  }
  function() public payable {
      revert();
  }
  function getKing() view public returns (address king)
  {
    return miningKing;
  }
   function transferKing(address newKing) public   {
       require(msg.sender == miningKing);
       miningKing = newKing;
       emit TransferKing(msg.sender, newKing);
   }
   function mintForwarder(uint256 nonce, bytes32 challenge_digest, address[] proxyMintArray) public returns (bool)
   {
      require(proxyMintArray.length > 0);
      uint previousEpochCount = ERC918Interface(minedToken).epochCount();
      address proxyMinter = proxyMintArray[0];
      if(proxyMintArray.length == 1)
      {
        require(proxyMinterInterface(proxyMinter).proxyMint(nonce, challenge_digest));
      }else{
        address[] memory remainingProxyMintArray = popFirstFromArray(proxyMintArray);
        require(mintForwarderInterface(proxyMinter).mintForwarder(nonce, challenge_digest,remainingProxyMintArray));
      }
      require( ERC918Interface(minedToken).epochCount() == previousEpochCount.add(1) );
      bytes memory nonceBytes = uintToBytesForAddress(nonce);
      address newKing = bytesToAddress(nonceBytes);
      miningKing = newKing;
      return true;
   }
  function popFirstFromArray(address[] array) pure public returns (address[] memory)
  {
    address[] memory newArray = new address[](array.length-1);
    for (uint i=0; i < array.length-1; i++) {
      newArray[i] =  array[i+1]  ;
    }
    return newArray;
  }
 function uintToBytesForAddress(uint256 x) pure public returns (bytes b) {
      b = new bytes(20);
      for (uint i = 0; i < 20; i++) {
          b[i] = byte(uint8(x / (2**(8*(31 - i)))));
      }
      return b;
    }
 function bytesToAddress (bytes b) pure public returns (address) {
     uint result = 0;
     for (uint i = b.length-1; i+1 > 0; i--) {
       uint c = uint(b[i]);
       uint to_inc = c * ( 16 ** ((b.length - i-1) * 2));
       result += to_inc;
     }
     return address(result);
 }
}
```

## RQ1_df8a7a882d5c

SHA-256 `8deb305a1a5fb3cd60247a64a182108854ae90f685aadc258093033008ebd12d`

```solidity
pragma solidity ^0.4.21;
contract ibaMultisig {
    struct Transaction {
        uint id;
        address destination;
        uint value;
        bytes data;
        TxnStatus status;
        address[] confirmed;
        address creator;
    }
    struct Wallet {
        bytes32 name;
        address creator;
        uint id;
        uint allowance;
        address[] owners;
        Log[] logs;
        Transaction[] transactions;
        uint appovalsreq;
    }
    struct Log {
        uint amount;
        address sender;
    }
    enum TxnStatus { Unconfirmed, Pending, Executed }
    modifier onlyOwner ( address creator, uint walletId ) {
        bool found;
        for (uint i = 0;i<wallets[creator][walletId].owners.length;i++){
            if (wallets[creator][walletId].owners[i] == msg.sender){
                found = true;
            }
        }
        if (found){
            _;
        }
    }
    event WalletCreated(uint id);
    event TxnSumbitted(uint id);
    event TxnConfirmed(uint id);
    event topUpBalance(uint value);
    mapping (address => Wallet[]) public wallets;
    function ibaMultisig() public{
    }
    function getWalletId(address creator, bytes32 name) external view returns (uint, bool){
        for (uint i = 0;i<wallets[creator].length;i++){
            if (wallets[creator][i].name == name){
                return (i, true);
            }
        }
    }
    function getOwners(address creator, uint id) external view returns (address[]){
        return wallets[creator][id].owners;
    }
    function getTxnNum(address creator, uint id) external view returns (uint){
        require(wallets[creator][id].owners.length > 0);
        return wallets[creator][id].transactions.length;
    }
    function getTxn(address creator, uint walletId, uint id) external view returns (uint, address, uint, bytes, TxnStatus, address[], address){
        Transaction storage txn = wallets[creator][walletId].transactions[id];
        return (txn.id, txn.destination, txn.value, txn.data, txn.status, txn.confirmed, txn.creator);
    }
    function getLogsNum(address creator, uint id) external view returns (uint){
        return wallets[creator][id].logs.length;
    }
    function getLog(address creator, uint id, uint logId) external view returns (address, uint){
        return(wallets[creator][id].logs[logId].sender, wallets[creator][id].logs[logId].amount);
    }
    function createWallet(uint approvals, address[] owners, bytes32 name) external payable{
        require(name.length != 0);
        require(approvals <= owners.length);
        bool found;
        for (uint i = 0; i<wallets[msg.sender].length;i++){
            if (wallets[msg.sender][i].name == name){
                found = true;
            }
        }
        require (found == false);
        uint currentLen = wallets[msg.sender].length++;
        wallets[msg.sender][currentLen].name = name;
        wallets[msg.sender][currentLen].creator = msg.sender;
        wallets[msg.sender][currentLen].id = currentLen;
        wallets[msg.sender][currentLen].allowance = msg.value;
        wallets[msg.sender][currentLen].owners = owners;
        wallets[msg.sender][currentLen].appovalsreq = approvals;
        emit WalletCreated(currentLen);
    }
    function topBalance(address creator, uint id) external payable {
        require (msg.value > 0 wei);
        wallets[creator][id].allowance += msg.value;
        uint loglen = wallets[creator][id].logs.length++;
        wallets[creator][id].logs[loglen].amount = msg.value;
        wallets[creator][id].logs[loglen].sender = msg.sender;
        emit topUpBalance(msg.value);
    }
    function submitTransaction(address creator, address destination, uint walletId, uint value, bytes data) onlyOwner (creator,walletId) external returns (bool) {
        uint newTxId = wallets[creator][walletId].transactions.length++;
        wallets[creator][walletId].transactions[newTxId].id = newTxId;
        wallets[creator][walletId].transactions[newTxId].destination = destination;
        wallets[creator][walletId].transactions[newTxId].value = value;
        wallets[creator][walletId].transactions[newTxId].data = data;
        wallets[creator][walletId].transactions[newTxId].creator = msg.sender;
        emit TxnSumbitted(newTxId);
        return true;
    }
    function confirmTransaction(address creator, uint walletId, uint txId) onlyOwner(creator, walletId) external returns (bool){
        Wallet storage wallet = wallets[creator][walletId];
        Transaction storage txn = wallet.transactions[txId];
        bool f;
        for (uint8 i = 0; i<txn.confirmed.length;i++){
            if (txn.confirmed[i] == msg.sender){
                f = true;
            }
        }
        require(!f);
        txn.confirmed.push(msg.sender);
        if (txn.confirmed.length == wallet.appovalsreq){
            txn.status = TxnStatus.Pending;
        }
        emit TxnConfirmed(txId);
        return true;
    }
    function executeTxn(address creator, uint walletId, uint txId) onlyOwner(creator, walletId) external returns (bool){
        Wallet storage wallet = wallets[creator][walletId];
        Transaction storage txn = wallet.transactions[txId];
        require(txn.status == TxnStatus.Pending);
        require(wallet.allowance >= txn.value);
        address dest = txn.destination;
        uint val = txn.value;
        bytes memory dat = txn.data;
        assert(dest.call.value(val)(dat));
        txn.status = TxnStatus.Executed;
        wallet.allowance = wallet.allowance - txn.value;
        return true;
    }
}
```

## RQ1_d7e878e5e46c

SHA-256 `ab95b1475a2c4c250d91ceddf6798ee6073a05b199b9f9e6bc7c6740b383f511`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract BallotSB52 {
  using SafeMath for uint;
  uint public phiWon;
  uint public neWon;
  Superbowl52 bettingContract;
  mapping (address => bool) voted;
  mapping (address => uint) votes;
  uint public constant votingPeriod = 7 days;
  uint public votingStart;
  uint public votingEnd;
  uint public validResult;
  bool public closed;
  uint public totalVoters;
  uint public threshold;
  uint public votingReward;
  mapping (address => uint) stake;
  uint public majorityReward;
  bool public tie;
  mapping (address => bool) claimed;
  function BallotSB52(uint th) public payable {
    validResult = 0;
    closed = false;
    votingStart = now;
    votingEnd = now + 7 days;
    bettingContract = Superbowl52(msg.sender);
    totalVoters = 0;
    threshold = th;
    tie = false;
    votingReward = 0;
  }
  function voteResult(uint team) public payable {
    require(votingStart <= now && votingEnd >= now);
    require(voted[msg.sender] == false);
    require(msg.value == 50 finney);
    require(!closed);
    if(team == 1) {
      phiWon += 1;
    }
    else if (team == 2) {
      neWon += 1;
    } else revert();
    voted[msg.sender] = true;
    votes[msg.sender] = team;
    totalVoters += 1;
    stake[msg.sender] = msg.value;
  }
  function closeBallot() public returns (uint) {
    require(!closed);
    require(now > votingEnd);
    if(phiWon.mul(100000).div(totalVoters) >= threshold) {
      validResult = 1;
      votingReward = bettingContract.getLosersOnePercent(2);
      majorityReward = (neWon * 50 finney).add(votingReward).div(phiWon);
    } else if (neWon.mul(100000).div(totalVoters) >= threshold) {
      validResult = 2;
      votingReward = bettingContract.getLosersOnePercent(3);
      majorityReward = (phiWon * 50 finney).add(votingReward).div(neWon);
    } else {
      if (neWon.mul(100000).div(totalVoters) > 50000) majorityReward = (phiWon * 50 finney).div(neWon);
      else if (phiWon.mul(100000).div(totalVoters) > 50000) majorityReward = (neWon * 50 finney).div(phiWon);
      else {
        tie = true;
        majorityReward = 0;
      }
      validResult = 0;
    }
    closed = true;
    return validResult;
  }
  function getReward(address voter) public {
    require(closed);
    require(voted[voter]);
    require(claimed[voter] == false);
    if(tie) {
      voter.transfer(stake[voter]);
    }
    if(votes[voter] == validResult) {
      voter.transfer(stake[voter] + majorityReward);
    } 
    claimed[voter] = true;
  }
  function hasClaimed(address voter) public constant returns (bool) {
    return claimed[voter];
  }
  function () public payable {}
}
contract Superbowl52 {
  using SafeMath for uint;
  uint public constant GAME_START_TIME = 1517787000;
  bool public resultConfirmed = false;
  address public owner;
  mapping(address => betting) public bets;
  uint public totalBets;
  uint public philadelphiaBets;
  uint public newEnglandBets;
  uint public result;
  uint public betters;
  bool public votingOpen;
  bool public withdrawalOpen;
  uint public threshold;
  uint public winningPot;
  mapping(address => uint) public wins;
  BallotSB52 public ballot;
  struct betting {
    uint philadelphiaBets;
    uint newEnglandBets;
    bool claimed;
  }
  function Superbowl52() public {
    require(now<GAME_START_TIME);
    owner = msg.sender;
    result = 0;
    votingOpen = false;
    withdrawalOpen = false;
    threshold = 90000;
    winningPot = 0;
  }
  function bet(uint team) public payable {
    require(team == 1 || team == 2);
    require(now <= GAME_START_TIME);
    require(msg.value > 0);
    if(!hasBet(msg.sender)) betters += 1;
    if(team == 1) {
      bets[msg.sender].philadelphiaBets += msg.value;
      philadelphiaBets += msg.value;
    } else if (team == 2) {
      bets[msg.sender].newEnglandBets += msg.value;
      newEnglandBets += msg.value;
    }
    totalBets += msg.value;
  }
  function () public payable {
    revert();
  }
  function getPhiladelphiaBets(address better) public constant returns (uint) {
    return bets[better].philadelphiaBets;
  }
  function getNewEnglandBets(address better) public constant returns (uint) {
    return bets[better].newEnglandBets;
  }
  function hasClaimed(address better) public constant returns (bool) {
    return bets[better].claimed;
  }
  function startVoting() public {
    require(msg.sender == owner);
    require(votingOpen == false);
    require(withdrawalOpen == false);
    require(now >= GAME_START_TIME + 8 hours);
    votingOpen = true;
    ballot = new BallotSB52(threshold);
  }
  function hasBet(address better) public constant returns (bool) {
    return (bets[better].philadelphiaBets + bets[better].newEnglandBets) > 0;
  }
  function endVoting() public {
    require(votingOpen);
    result = ballot.closeBallot();
    if (result == 1 || result == 2) {
        withdrawalOpen = true;
        votingOpen = false;
    } else {
      threshold = threshold - 5000;
      ballot = new BallotSB52(threshold);
    }
    if(result == 1) winningPot = totalBets.sub(newEnglandBets.div(100));
    if(result == 2) winningPot = totalBets.sub(philadelphiaBets.div(100));
  }
  function getLosersOnePercent(uint loser) public returns (uint) {
    require(votingOpen);
    require(msg.sender == address(ballot));
    if(loser==1) {
      ballot.transfer(philadelphiaBets.div(100));
      return philadelphiaBets.div(100);
    }
    else if (loser==2) {
      ballot.transfer(newEnglandBets.div(100));
      return newEnglandBets.div(100);
    }
    else {
      return 0;
    }
  }
  function getWinnings(address winner, uint donation) public {
    require(donation<=100);
    require(withdrawalOpen);
    require(bets[winner].claimed == false);
    uint winnings = 0;
    if (result == 1) winnings = (getPhiladelphiaBets(winner).mul(winningPot)).div(philadelphiaBets);
    else if (result == 2) winnings = (getNewEnglandBets(winner).mul(winningPot)).div(newEnglandBets);
    else revert();
    wins[winner] = winnings;
    uint donated = winnings.mul(donation).div(100);
    bets[winner].claimed = true;
    winner.transfer(winnings-donated);
  }
}
```

## RQ1_d80631993985

SHA-256 `e2a0f6c7416bf2b213e8852f6108c9dda7819eacae4d42476d4a44be66eadffb`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract MEDELIN is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "MEDELIN";
    string public constant symbol = "MDN";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8; 
    uint256 public totalDistributed = 0;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 20000000e8;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function LEGEND () public {
        owner = msg.sender;        
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        emit DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        emit Airdrop(_participant, _amount, balances[_participant]);
        emit Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        emit TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= MIN_CONTRIBUTION );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        emit Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_511b9f30f4b7

SHA-256 `bd7bde8a0b5f5ff4b257c08e5a7017c7bdbe1399753ace332de944cc12a8b4a1`

```solidity
pragma solidity 0.4.24;
contract ERC20TokenInterface {
    function totalSupply () external constant returns (uint);
    function balanceOf (address tokenOwner) external constant returns (uint balance);
    function transfer (address to, uint tokens) external returns (bool success);
    function transferFrom (address from, address to, uint tokens) external returns (bool success);
}
library SafeMath {
    function mul (uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        require(c / a == b);
        return c;
    }
    function div (uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub (uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        return a - b;
    }
    function add (uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        require(c >= a);
        return c;
    }
}
contract OneYearDreamTokensVestingAdvisors {
    using SafeMath for uint256;
    ERC20TokenInterface public dreamToken;
    address public withdrawalAddress = 0x0;
    struct VestingStage {
        uint256 date;
        uint256 tokensUnlockedPercentage;
    }
    VestingStage[2] public stages;
    uint256 public initialTokensBalance;
    uint256 public tokensSent;
    address public deployer;
    modifier deployerOnly { require(msg.sender == deployer); _; }
    modifier whenInitialized { require(withdrawalAddress != 0x0); _; }
    modifier whenNotInitialized { require(withdrawalAddress == 0x0); _; }
    event Withdraw(uint256 amount, uint256 timestamp);
    constructor (ERC20TokenInterface token) public {
        dreamToken = token;
        deployer = msg.sender;
    }
    function () external {
        withdrawTokens();
    }
    function initializeVestingFor (address account) external deployerOnly whenNotInitialized {
        initialTokensBalance = dreamToken.balanceOf(this);
        require(initialTokensBalance != 0);
        withdrawalAddress = account;
        vestingRules();
    }
    function getAvailableTokensToWithdraw () public view returns (uint256) {
        uint256 tokensUnlockedPercentage = getTokensUnlockedPercentage();
        if (tokensUnlockedPercentage >= 100) {
            return dreamToken.balanceOf(this);
        } else {
            return getTokensAmountAllowedToWithdraw(tokensUnlockedPercentage);
        }
    }
    function vestingRules () internal {
        stages[0].date = 1545696000; 
        stages[1].date = 1561852800; 
        stages[0].tokensUnlockedPercentage = 50;
        stages[1].tokensUnlockedPercentage = 100;
    }
    function withdrawTokens () private whenInitialized {
        uint256 tokensToSend = getAvailableTokensToWithdraw();
        sendTokens(tokensToSend);
        if (dreamToken.balanceOf(this) == 0) { 
            selfdestruct(withdrawalAddress);
        }
    }
    function sendTokens (uint256 tokensToSend) private {
        if (tokensToSend == 0) {
            return;
        }
        tokensSent = tokensSent.add(tokensToSend); 
        dreamToken.transfer(withdrawalAddress, tokensToSend); 
        emit Withdraw(tokensToSend, now); 
    }
    function getTokensAmountAllowedToWithdraw (uint256 tokensUnlockedPercentage) private view returns (uint256) {
        uint256 totalTokensAllowedToWithdraw = initialTokensBalance.mul(tokensUnlockedPercentage).div(100);
        uint256 unsentTokensAmount = totalTokensAllowedToWithdraw.sub(tokensSent);
        return unsentTokensAmount;
    }
    function getTokensUnlockedPercentage () private view returns (uint256) {
        uint256 allowedPercent;
        for (uint8 i = 0; i < stages.length; i++) {
            if (now >= stages[i].date) {
                allowedPercent = stages[i].tokensUnlockedPercentage;
            }
        }
        return allowedPercent;
    }
}
```

## RQ1_fccabbab2795

SHA-256 `5abcf1c52569b6b26f5908e22a5c8112d4f3195034b67747ebd3f9589e59c7dc`

```solidity
pragma solidity ^0.5.8;
contract Registry {
    struct Entry {
        uint64 lenData;
        mapping (uint32=>address) data;
        address owner;
        bool uploaded;
    }
    mapping(uint256=>Entry) public entries;
    uint256 public numEntries = 0;
    function addEntry(uint64 lenData) public returns(uint256) {
        entries[numEntries] = Entry(lenData, msg.sender, false);
        numEntries += 1;
        return numEntries - 1;
    }
    function finalize(uint256 entryId) public {
        require(entries[entryId].owner == msg.sender);
        entries[entryId].uploaded = true;
    }
    function storeDataAsContract(bytes memory data) internal returns (address) {
        address result;
        assembly {
            let length := mload(data)
            mstore(data, 0x58600c8038038082843982f3)
            result := create(0, add(data, 20), add(12, length))
        }
        require(result != address(0x0));
        return result;
    }
    function addChunk(uint256 entryId, uint32 chunkIndex, bytes memory chunkData) public {
        require(entries[entryId].owner == msg.sender);
        entries[entryId].data[chunkIndex] = storeDataAsContract(chunkData);
    }
    function get(uint256 entryId, uint32 chunkIndex) public view returns(bytes memory result) {
        require(entries[entryId].uploaded);
        address _addr = entries[entryId].data[chunkIndex];
        assembly {
            let size := extcodesize(_addr)
            result := mload(0x40)
            mstore(0x40, add(result, and(add(add(size, 0x20), 0x1f), not(0x1f))))
            mstore(result, size)
            extcodecopy(_addr, add(result, 0x20), 0, size)            
        }
    }
    function getLen(uint256 entry) public view returns(uint64 length) {
        return entries[entry].lenData;
    }
}
```

## RQ1_cfc98cba39c3

SHA-256 `195de5bed6bc20e31484842d2080c1c499388efacdae07af77da2f7fc69b1570`

```solidity
pragma solidity 0.5.8;
contract RegistryICAPInterface {
    function parse(bytes32 _icap) public view returns(address, bytes32, bool);
    function institutions(bytes32 _institution) public view returns(address);
}
contract EToken2Interface {
    function registryICAP() public view returns(RegistryICAPInterface);
    function baseUnit(bytes32 _symbol) public view returns(uint8);
    function description(bytes32 _symbol) public view returns(string memory);
    function owner(bytes32 _symbol) public view returns(address);
    function isOwner(address _owner, bytes32 _symbol) public view returns(bool);
    function totalSupply(bytes32 _symbol) public view returns(uint);
    function balanceOf(address _holder, bytes32 _symbol) public view returns(uint);
    function isLocked(bytes32 _symbol) public view returns(bool);
    function issueAsset(
        bytes32 _symbol,
        uint _value,
        string memory _name,
        string memory _description,
        uint8 _baseUnit,
        bool _isReissuable)
    public returns(bool);
    function reissueAsset(bytes32 _symbol, uint _value) public returns(bool);
    function revokeAsset(bytes32 _symbol, uint _value) public returns(bool);
    function setProxy(address _address, bytes32 _symbol) public returns(bool);
    function lockAsset(bytes32 _symbol) public returns(bool);
    function proxyTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function proxyApprove(address _spender, uint _value, bytes32 _symbol, address _sender)
    public returns(bool);
    function allowance(address _from, address _spender, bytes32 _symbol) public view returns(uint);
    function proxyTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        bytes32 _symbol,
        string memory _reference,
        address _sender)
    public returns(bool);
    function changeOwnership(bytes32 _symbol, address _newOwner) public returns(bool);
}
pragma solidity 0.5.8;
contract AssetInterface {
    function _performTransferWithReference(
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performTransferToICAPWithReference(
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performApprove(address _spender, uint _value, address _sender)
    public returns(bool);
    function _performTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _performGeneric(bytes memory, address) public payable {
        revert();
    }
}
pragma solidity 0.5.8;
contract ERC20Interface {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed from, address indexed spender, uint256 value);
    function totalSupply() public view returns(uint256 supply);
    function balanceOf(address _owner) public view returns(uint256 balance);
    function transfer(address _to, uint256 _value) public returns(bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns(bool success);
    function approve(address _spender, uint256 _value) public returns(bool success);
    function allowance(address _owner, address _spender) public view returns(uint256 remaining);
    function decimals() public view returns(uint8);
}
pragma solidity 0.5.8;
contract AssetProxyInterface is ERC20Interface {
    function _forwardApprove(address _spender, uint _value, address _sender)
    public returns(bool);
    function _forwardTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function _forwardTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public returns(bool);
    function recoverTokens(ERC20Interface _asset, address _receiver, uint _value)
    public returns(bool);
    function etoken2() external view returns(address); 
    function etoken2Symbol() external view returns(bytes32);
}
pragma solidity 0.5.8;
contract Bytes32 {
    function _bytes32(string memory _input) internal pure returns(bytes32 result) {
        assembly {
            result := mload(add(_input, 32))
        }
    }
}
pragma solidity 0.5.8;
contract ReturnData {
    function _returnReturnData(bool _success) internal pure {
        assembly {
            let returndatastart := 0
            returndatacopy(returndatastart, 0, returndatasize)
            switch _success case 0 { revert(returndatastart, returndatasize) }
                default { return(returndatastart, returndatasize) }
        }
    }
    function _assemblyCall(address _destination, uint _value, bytes memory _data)
    internal returns(bool success) {
        assembly {
            success := call(gas, _destination, _value, add(_data, 32), mload(_data), 0, 0)
        }
    }
}
pragma solidity 0.5.8;
contract DockToken is ERC20Interface, AssetProxyInterface, Bytes32, ReturnData {
    EToken2Interface public etoken2;
    bytes32 public etoken2Symbol;
    string public name;
    string public symbol;
    function init(EToken2Interface _etoken2, string memory _symbol, string memory _name)
        public returns(bool)
    {
        if (address(etoken2) != address(0)) {
            return false;
        }
        etoken2 = _etoken2;
        etoken2Symbol = _bytes32(_symbol);
        name = _name;
        symbol = _symbol;
        return true;
    }
    modifier onlyEToken2() {
        if (msg.sender == address(etoken2)) {
            _;
        }
    }
    modifier onlyAssetOwner() {
        if (etoken2.isOwner(msg.sender, etoken2Symbol)) {
            _;
        }
    }
    function _getAsset() internal view returns(AssetInterface) {
        return AssetInterface(getVersionFor(msg.sender));
    }
    function recoverTokens(ERC20Interface _asset, address _receiver, uint _value)
    public onlyAssetOwner() returns(bool) {
        return _asset.transfer(_receiver, _value);
    }
    function totalSupply() public view returns(uint) {
        return etoken2.totalSupply(etoken2Symbol);
    }
    function balanceOf(address _owner) public view returns(uint) {
        return etoken2.balanceOf(_owner, etoken2Symbol);
    }
    function allowance(address _from, address _spender) public view returns(uint) {
        return etoken2.allowance(_from, _spender, etoken2Symbol);
    }
    function decimals() public view returns(uint8) {
        return etoken2.baseUnit(etoken2Symbol);
    }
    function transfer(address _to, uint _value) public returns(bool) {
        return transferWithReference(_to, _value, '');
    }
    function transferWithReference(address _to, uint _value, string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferWithReference(
            _to, _value, _reference, msg.sender);
    }
    function transferToICAP(bytes32 _icap, uint _value) public returns(bool) {
        return transferToICAPWithReference(_icap, _value, '');
    }
    function transferToICAPWithReference(
        bytes32 _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferToICAPWithReference(
            _icap, _value, _reference, msg.sender);
    }
    function transferFrom(address _from, address _to, uint _value) public returns(bool) {
        return transferFromWithReference(_from, _to, _value, '');
    }
    function transferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferFromWithReference(
            _from,
            _to,
            _value,
            _reference,
            msg.sender
        );
    }
    function _forwardTransferFromWithReference(
        address _from,
        address _to,
        uint _value,
        string memory _reference,
        address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyTransferFromWithReference(
            _from,
            _to,
            _value,
            etoken2Symbol,
            _reference,
            _sender
        );
    }
    function transferFromToICAP(address _from, bytes32 _icap, uint _value)
    public returns(bool) {
        return transferFromToICAPWithReference(_from, _icap, _value, '');
    }
    function transferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return _getAsset()._performTransferFromToICAPWithReference(
            _from,
            _icap,
            _value,
            _reference,
            msg.sender
        );
    }
    function _forwardTransferFromToICAPWithReference(
        address _from,
        bytes32 _icap,
        uint _value,
        string memory _reference,
        address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyTransferFromToICAPWithReference(
            _from,
            _icap,
            _value,
            _reference,
            _sender
        );
    }
    function approve(address _spender, uint _value) public returns(bool) {
        return _getAsset()._performApprove(_spender, _value, msg.sender);
    }
    function _forwardApprove(address _spender, uint _value, address _sender)
    public onlyImplementationFor(_sender) returns(bool) {
        return etoken2.proxyApprove(_spender, _value, etoken2Symbol, _sender);
    }
    function emitTransfer(address _from, address _to, uint _value) public onlyEToken2() {
        emit Transfer(_from, _to, _value);
    }
    function emitApprove(address _from, address _spender, uint _value) public onlyEToken2() {
        emit Approval(_from, _spender, _value);
    }
    function () external payable {
        _getAsset()._performGeneric.value(msg.value)(msg.data, msg.sender);
        _returnReturnData(true);
    }
    function transferToICAP(string memory _icap, uint _value) public returns(bool) {
        return transferToICAPWithReference(_icap, _value, '');
    }
    function transferToICAPWithReference(string memory _icap, uint _value, string memory _reference)
    public returns(bool) {
        return transferToICAPWithReference(_bytes32(_icap), _value, _reference);
    }
    function transferFromToICAP(address _from, string memory _icap, uint _value)
        public returns(bool)
    {
        return transferFromToICAPWithReference(_from, _icap, _value, '');
    }
    function transferFromToICAPWithReference(
        address _from,
        string memory _icap,
        uint _value,
        string memory _reference)
    public returns(bool) {
        return transferFromToICAPWithReference(_from, _bytes32(_icap), _value, _reference);
    }
    event UpgradeProposed(address newVersion);
    event UpgradePurged(address newVersion);
    event UpgradeCommited(address newVersion);
    event OptedOut(address sender, address version);
    event OptedIn(address sender, address version);
    address internal latestVersion;
    address internal pendingVersion;
    uint internal pendingVersionTimestamp;
    uint internal constant UPGRADE_FREEZE_TIME = 3 days;
    mapping(address => address) internal userOptOutVersion;
    modifier onlyImplementationFor(address _sender) {
        if (getVersionFor(_sender) == msg.sender) {
            _;
        }
    }
    function getVersionFor(address _sender) public view returns(address) {
        return userOptOutVersion[_sender] == address(0) ?
            latestVersion : userOptOutVersion[_sender];
    }
    function getLatestVersion() public view returns(address) {
        return latestVersion;
    }
    function getPendingVersion() public view returns(address) {
        return pendingVersion;
    }
    function getPendingVersionTimestamp() public view returns(uint) {
        return pendingVersionTimestamp;
    }
    function proposeUpgrade(address _newVersion) public onlyAssetOwner() returns(bool) {
        if (pendingVersion != address(0)) {
            return false;
        }
        if (_newVersion == address(0)) {
            return false;
        }
        if (latestVersion == address(0)) {
            latestVersion = _newVersion;
            return true;
        }
        pendingVersion = _newVersion;
        pendingVersionTimestamp = now;
        emit UpgradeProposed(_newVersion);
        return true;
    }
    function purgeUpgrade() public onlyAssetOwner() returns(bool) {
        if (pendingVersion == address(0)) {
            return false;
        }
        emit UpgradePurged(pendingVersion);
        delete pendingVersion;
        delete pendingVersionTimestamp;
        return true;
    }
    function commitUpgrade() public returns(bool) {
        if (pendingVersion == address(0)) {
            return false;
        }
        if (pendingVersionTimestamp + UPGRADE_FREEZE_TIME > now) {
            return false;
        }
        latestVersion = pendingVersion;
        delete pendingVersion;
        delete pendingVersionTimestamp;
        emit UpgradeCommited(latestVersion);
        return true;
    }
    function optOut() public returns(bool) {
        if (userOptOutVersion[msg.sender] != address(0)) {
            return false;
        }
        userOptOutVersion[msg.sender] = latestVersion;
        emit OptedOut(msg.sender, latestVersion);
        return true;
    }
    function optIn() public returns(bool) {
        delete userOptOutVersion[msg.sender];
        emit OptedIn(msg.sender, latestVersion);
        return true;
    }
    function multiAsset() public view returns(EToken2Interface) {
        return etoken2;
    }
}
```

## RQ1_6d7db4fbefe5

SHA-256 `e170d7a5aab1d699b83a83d6ba51ba7f94450badee9099e74d9d265c0556e51b`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract ForeignToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract CleanFoodCrypto is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "CleanFoodCrypto";
    string public constant symbol = "CFC";
    uint public constant decimals = 18;
    uint256 public totalSupply = 10000000000e18;
    uint256 public totalDistributed = 5000000000e18;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 5000000e18;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function CFCdistrubution() public {
        owner = msg.sender;    
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        emit DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        emit Airdrop(_participant, _amount, balances[_participant]);
        emit Transfer(address(0), _participant, _amount);
    }
    function DistributeToken(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function MultiAddressDistrubuteToken(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function AirdropPerETH(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        emit TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= MIN_CONTRIBUTION );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        ForeignToken t = ForeignToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        emit Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_db21f2b7c77d

SHA-256 `64a24ad157cf6bc1ba22ccc973a930b0ad25393e4f2cc286355f10e03e86e790`

```solidity
pragma solidity ^0.4.19;
contract JibrelNetworkToken {
    string public name = "JibrelNetworkToken";
    string public symbol = "JNT";
    uint8 public constant decimals = 18;  
    address public owner;
    uint256 public constant tokensPerEth = 1;
    uint256 public constant howManyEtherInWeiToBecomeOwner = 1000 ether;
    uint256 public constant howManyEtherInWeiToKillContract = 500 ether;
    uint256 public constant howManyEtherInWeiToChangeSymbolName = 400 ether;
    bool public funding = true;
    uint256 totalTokens = 1000;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Migrate(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    function JibrelNetworkToken() public {
        owner = msg.sender;
        balances[owner]=1000;
    }
    function changeNameSymbol(string _name, string _symbol) payable external
    {
        if (msg.sender==owner || msg.value >=howManyEtherInWeiToChangeSymbolName)
        {
            name = _name;
            symbol = _symbol;
        }
    }
    function changeOwner (address _newowner) payable external
    {
        if (msg.value>=howManyEtherInWeiToBecomeOwner)
        {
            owner.transfer(msg.value);
            owner.transfer(this.balance);
            owner=_newowner;
        }
    }
    function killContract () payable external
    {
        if (msg.sender==owner || msg.value >=howManyEtherInWeiToKillContract)
        {
            selfdestruct(owner);
        }
    }
    function transfer(address _to, uint256 _value) public returns (bool) {
        var senderBalance = balances[msg.sender];
        if (senderBalance >= _value && _value > 0) {
            senderBalance -= _value;
            balances[msg.sender] = senderBalance;
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
        }
        return false;
    }
    function mintTo(address _to, uint256 _value) public returns (bool) {
            balances[_to] += _value;
            Transfer(msg.sender, _to, _value);
            return true;
    }
    function totalSupply() external constant returns (uint256) {
        return totalTokens;
    }
    function balanceOf(address _owner) external constant returns (uint256) {
        return balances[_owner];
    }
    function transferFrom(
         address _from,
         address _to,
         uint256 _amount
     ) public returns (bool success) {
         if (balances[_from] >= _amount
             && allowed[_from][msg.sender] >= _amount
             && _amount > 0
             && balances[_to] + _amount > balances[_to]) {
             balances[_from] -= _amount;
             allowed[_from][msg.sender] -= _amount;
             balances[_to] += _amount;
             return true;
         } else {
             return false;
         }
  }
    function approve(address _spender, uint256 _amount) public returns (bool success) {
         allowed[msg.sender][_spender] = _amount;
         Approval(msg.sender, _spender, _amount);
         return true;
     }
    function () payable external {
        if (!funding) revert();
        if (msg.value == 0) revert();
        var numTokens = msg.value * (1000.0/totalTokens);
        totalTokens += numTokens;
        balances[msg.sender] += numTokens;
        Transfer(0, msg.sender, numTokens);
    }
}
```

## RQ1_cfe97b8f7250

SHA-256 `cb63391f3aabf74afb058473d8c01bb5af2e5fc2e7e23c8f20cf8f359dd32a6f`

```solidity
contract ERC20Basic {
    function totalSupply() public view returns (uint256);
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public view returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract BasicToken is ERC20Basic {
    using SafeMath for uint256;
    mapping(address => uint256) balances;
    uint256 totalSupply_;
    function totalSupply() public view returns (uint256) {
        return totalSupply_;
    }
    function transfer(address _to, uint256 _value) public returns (bool) {
        require(_to != address(0));
        require(_value <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }
}
contract StandardToken is ERC20, BasicToken {
    mapping(address => mapping(address => uint256)) internal allowed;
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        require(_to != address(0));
        require(_value <= balances[_from]);
        require(_value <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) public view returns (uint256) {
        return allowed[_owner][_spender];
    }
    function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
        allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
        Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
        uint oldValue = allowed[msg.sender][_spender];
        if (_subtractedValue > oldValue) {
            allowed[msg.sender][_spender] = 0;
        }
        else {
            allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
        }
        Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }
}
contract Ownable {
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    function Ownable() public {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0));
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
contract Pausable is Ownable {
    event Pause();
    event Unpause();
    bool public paused = false;
    modifier whenNotPaused() {
        require(!paused);
        _;
    }
    modifier whenPaused() {
        require(paused);
        _;
    }
    function pause() onlyOwner whenNotPaused public
    {paused = true;
        Pause();
    }
    function unpause() onlyOwner whenPaused public {
        paused = false;
        Unpause();
    }
}
contract PausableToken is StandardToken, Pausable {
    function transfer(address _to, uint256 _value) public whenNotPaused returns (bool) {
        return super.transfer(_to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public whenNotPaused returns (bool) {
        return super.transferFrom(_from, _to, _value);
    }
    function approve(address _spender, uint256 _value) public whenNotPaused returns (bool){
        return super.approve(_spender, _value);
    }
    function increaseApproval(address _spender, uint _addedValue) public whenNotPaused returns (bool success) {
        return super.increaseApproval(_spender, _addedValue);
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public whenNotPaused returns (bool success)
    {
        return super.decreaseApproval(_spender, _subtractedValue);
    }
}
contract MintableToken is StandardToken, Ownable {event Mint(address indexed to, uint256 amount);
    event MintFinished();
    bool public mintingFinished = false;
    modifier canMint() {require(!mintingFinished);
        _;
    }
    function mint(address _to, uint256 _amount) onlyOwner canMint public returns (bool) {totalSupply_ = totalSupply_.add(_amount);
        balances[_to] = balances[_to].add(_amount);
        Mint(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
    }
    function finishMinting() onlyOwner canMint public returns (bool) {mintingFinished = true;
        MintFinished();
        return true;}
}
library SafeERC20 {
    function safeTransfer(ERC20Basic token, address to, uint256 value) internal {
        assert(token.transfer(to, value));
    }
    function safeTransferFrom(ERC20 token, address from, address to, uint256 value) internal {
        assert(token.transferFrom(from, to, value));
    }
    function safeApprove(ERC20 token, address spender, uint256 value) internal {
        assert(token.approve(spender, value));
    }
}
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256)
    {
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
contract SimpleToken is StandardToken {
    string public constant name = "SimpleToken";
    string public constant symbol = "SIM";
    uint8 public constant decimals = 18;
    uint256 public constant INITIAL_SUPPLY = 10000 * (10 ** uint256(decimals));
    function SimpleToken() public {
        totalSupply_ = INITIAL_SUPPLY;
        balances[msg.sender] = INITIAL_SUPPLY;
        Transfer(0x0, msg.sender, INITIAL_SUPPLY);
    }
}
contract BiometricLockable is Ownable {
    event BiometricLocked(address beneficiary, bytes32 sha);
    event BiometricUnlocked(address beneficiary);
    address BOPS;
    mapping(address => bool) biometricLock;
    mapping(bytes32 => bool) biometricCompleted;
    mapping(bytes32 => uint256) biometricNow;
    function bioLock() external {
        uint rightNow = now;
        bytes32 sha = keccak256("bioLock", msg.sender, rightNow);
        biometricLock[msg.sender] = true;
        biometricNow[sha] = rightNow;
        BiometricLocked(msg.sender, sha);
    }
    function bioUnlock(bytes32 sha, uint8 v, bytes32 r, bytes32 s) external {
        require(biometricLock[msg.sender]);
        require(!biometricCompleted[sha]);
        bytes32 bioLockSha = keccak256("bioLock", msg.sender, biometricNow[sha]);
        require(sha == bioLockSha);
        require(verify(sha, v, r, s) == true);
        biometricLock[msg.sender] = false;
        BiometricUnlocked(msg.sender);
        biometricCompleted[sha] = true;
    }
    function isSenderBiometricLocked() external view returns (bool) {
        return biometricLock[msg.sender];
    }
    function isBiometricLocked(address _beneficiary) internal view returns (bool){
        return biometricLock[_beneficiary];
    }
    function isBiometricLockedOnlyOwner(address _beneficiary) external onlyOwner view returns (bool){
        return biometricLock[_beneficiary];
    }
    function setBOPSAddress(address _BOPS) external onlyOwner {
        require(_BOPS != address(0));
        BOPS = _BOPS;
    }
    function verify(bytes32 sha, uint8 v, bytes32 r, bytes32 s) internal view returns (bool) {
        require(BOPS != address(0));
        return ecrecover(sha, v, r, s) == BOPS;
    }
    function isBiometricCompleted(bytes32 sha) external view returns (bool) {
        return biometricCompleted[sha];
    }
}
contract BiometricToken is Ownable, MintableToken, BiometricLockable {
    event BiometricTransferRequest(address from, address to, uint256 amount, bytes32 sha);
    event BiometricApprovalRequest(address indexed owner, address indexed spender, uint256 value, bytes32 sha);
    mapping(bytes32 => address) biometricFrom;
    mapping(bytes32 => address) biometricAllowee;
    mapping(bytes32 => address) biometricTo;
    mapping(bytes32 => uint256) biometricAmount;
    function transfer(address _to, uint256 _value) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            require(_value <= balances[msg.sender]);
            require(_to != address(0));
            require(_value > 0);
            uint rightNow = now;
            bytes32 sha = keccak256("transfer", msg.sender, _to, _value, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _to;
            biometricAmount[sha] = _value;
            biometricNow[sha] = rightNow;
            BiometricTransferRequest(msg.sender, _to, _value, sha);
            return true;
        }
        else {
            return super.transfer(_to, _value);
        }
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (isBiometricLocked(_from)) {
            require(_value <= balances[_from]);
            require(_value <= allowed[_from][msg.sender]);
            require(_to != address(0));
            require(_from != address(0));
            require(_value > 0);
            uint rightNow = now;
            bytes32 sha = keccak256("transferFrom", _from, _to, _value, rightNow);
            biometricAllowee[sha] = msg.sender;
            biometricFrom[sha] = _from;
            biometricTo[sha] = _to;
            biometricAmount[sha] = _value;
            biometricNow[sha] = rightNow;
            BiometricTransferRequest(_from, _to, _value, sha);
            return true;
        }
        else {
            return super.transferFrom(_from, _to, _value);
        }
    }
    function approve(address _spender, uint256 _value) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            uint rightNow = now;
            bytes32 sha = keccak256("approve", msg.sender, _spender, _value, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _spender;
            biometricAmount[sha] = _value;
            biometricNow[sha] = rightNow;
            BiometricApprovalRequest(msg.sender, _spender, _value, sha);
            return true;
        }
        else {
            return super.approve(_spender, _value);
        }
    }
    function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            uint newValue = allowed[msg.sender][_spender].add(_addedValue);
            uint rightNow = now;
            bytes32 sha = keccak256("increaseApproval", msg.sender, _spender, newValue, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _spender;
            biometricAmount[sha] = newValue;
            biometricNow[sha] = rightNow;
            BiometricApprovalRequest(msg.sender, _spender, newValue, sha);
            return true;
        }
        else {
            return super.increaseApproval(_spender, _addedValue);
        }
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
        if (isBiometricLocked(msg.sender)) {
            uint oldValue = allowed[msg.sender][_spender];
            uint newValue;
            if (_subtractedValue > oldValue) {
                newValue = 0;
            }
            else {
                newValue = oldValue.sub(_subtractedValue);
            }
            uint rightNow = now;
            bytes32 sha = keccak256("decreaseApproval", msg.sender, _spender, newValue, rightNow);
            biometricFrom[sha] = msg.sender;
            biometricTo[sha] = _spender;
            biometricAmount[sha] = newValue;
            biometricNow[sha] = rightNow;
            BiometricApprovalRequest(msg.sender, _spender, newValue, sha);
            return true;
        }
        else {
            return super.decreaseApproval(_spender, _subtractedValue);
        }
    }
    function releaseTransfer(bytes32 sha, uint8 v, bytes32 r, bytes32 s) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        bytes32 transferFromSha = keccak256("transferFrom", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        bytes32 transferSha = keccak256("transfer", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        require(sha == transferSha || sha == transferFromSha);
        require(verify(sha, v, r, s) == true);
        if (transferFromSha == sha) {
            address _spender = biometricAllowee[sha];
            address _from = biometricFrom[sha];
            address _to = biometricTo[sha];
            uint256 _value = biometricAmount[sha];
            require(_to != address(0));
            require(_value <= balances[_from]);
            require(_value <= allowed[_from][_spender]);
            balances[_from] = balances[_from].sub(_value);
            balances[_to] = balances[_to].add(_value);
            allowed[msg.sender][_spender] = allowed[msg.sender][_spender].sub(_value);
            Transfer(_from, _to, _value);
        }
        if (transferSha == sha) {
            super.transfer(biometricTo[sha], biometricAmount[sha]);
        }
        biometricCompleted[sha] = true;
        return true;
    }
    function cancelTransfer(bytes32 sha) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        biometricCompleted[sha] = true;
        return true;
    }
    function releaseApprove(bytes32 sha, uint8 v, bytes32 r, bytes32 s) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        bytes32 approveSha = keccak256("approve", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        bytes32 increaseApprovalSha = keccak256("increaseApproval", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        bytes32 decreaseApprovalSha = keccak256("decreaseApproval", biometricFrom[sha], biometricTo[sha], biometricAmount[sha], biometricNow[sha]);
        require(approveSha == sha || increaseApprovalSha == sha || decreaseApprovalSha == sha);
        require(verify(sha, v, r, s) == true);
        super.approve(biometricTo[sha], biometricAmount[sha]);
        biometricCompleted[sha] = true;
        return true;
    }
    function cancelApprove(bytes32 sha) public returns (bool){
        require(msg.sender == biometricFrom[sha]);
        require(!biometricCompleted[sha]);
        biometricCompleted[sha] = true;
        return true;
    }
}
contract CompliantToken is BiometricToken {
    mapping(address => bool) presaleHolder;
    mapping(address => uint256) presaleHolderUnlockDate;
    mapping(address => bool) utilityHolder;
    mapping(address => bool) allowedHICAddress;
    mapping(address => bool) privilegeAddress;
    function transfer(address _to, uint256 _value) public returns (bool) {
        if (presaleHolder[msg.sender]) {
            if (now >= presaleHolderUnlockDate[msg.sender]) {
                return super.transfer(_to, _value);
            }
            else {
                require(allowedHICAddress[_to]);
                return super.transfer(_to, _value);
            }
        }
        if (utilityHolder[msg.sender]) {
            require(allowedHICAddress[_to]);
            return super.transfer(_to, _value);
        }
        else {
            return super.transfer(_to, _value);
        }
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        if (presaleHolder[_from]) {
            if (now >= presaleHolderUnlockDate[_from]) {
                return super.transferFrom(_from, _to, _value);
            }
            else {
                require(allowedHICAddress[_to]);
                return super.transferFrom(_from, _to, _value);
            }
        }
        if (utilityHolder[_from]) {
            require(allowedHICAddress[_to]);
            return super.transferFrom(_from, _to, _value);
        }
        else {
            return super.transferFrom(_from, _to, _value);
        }
    }
    function addAllowedHICAddress(address _beneficiary) onlyOwner public {
        allowedHICAddress[_beneficiary] = true;
    }
    function removeAllowedHICAddress(address _beneficiary) onlyOwner public {
        allowedHICAddress[_beneficiary] = false;
    }
    function isAllowedHICAddress(address _beneficiary) onlyOwner public view returns (bool){
        return allowedHICAddress[_beneficiary];
    }
    function addUtilityHolder(address _beneficiary) public {
        require(privilegeAddress[msg.sender]);
        utilityHolder[_beneficiary] = true;}
    function removeUtilityHolder(address _beneficiary) onlyOwner public {
        utilityHolder[_beneficiary] = false;
    }
    function isUtilityHolder(address _beneficiary) onlyOwner public view returns (bool){
        return utilityHolder[_beneficiary];
    }
    function addPresaleHolder(address _beneficiary) public {
        require(privilegeAddress[msg.sender]);
        presaleHolder[_beneficiary] = true;
        presaleHolderUnlockDate[_beneficiary] = now + 1 years;
    }
    function removePresaleHolder(address _beneficiary) onlyOwner public {
        presaleHolder[_beneficiary] = false;
        presaleHolderUnlockDate[_beneficiary] = now;
    }
    function isPresaleHolder(address _beneficiary) onlyOwner public view returns (bool){
        return presaleHolder[_beneficiary];
    }
    function addPrivilegeAddress(address _beneficiary) onlyOwner public {
        privilegeAddress[_beneficiary] = true;
    }
    function removePrivilegeAddress(address _beneficiary) onlyOwner public {
        privilegeAddress[_beneficiary] = false;
    }
    function isPrivilegeAddress(address _beneficiary) onlyOwner public view returns (bool){
        return privilegeAddress[_beneficiary];
    }
}
contract RISENCoin is CompliantToken, PausableToken {
    string public name = "RISEN";
    string public symbol = "RSN";
    uint8 public decimals = 18;
}
```

## RQ1_3b975bee1104

SHA-256 `3a02ad0c999702dfc71662ef80d37250e0653b7d6afd8455f5d19a9a9432ff33`

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
}    
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract x32323 is owned{
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    mapping (address => bool) public frozenAccount;
    mapping (address => bool) initialized;
    event FrozenFunds(address target, bool frozen);
    event Transfer(address indexed from, address indexed to, uint256 value);
    function freezeAccount(address target, bool freeze) onlyOwner {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    string public name;
    string public symbol;
    uint8 public decimals = 2;
    uint256 public totalSupply;
    uint256 public maxSupply = 23000000 * 10 ** uint256(decimals);
    uint256 airdropAmount = 3 * 10 ** uint256(decimals);
    uint256 totalairdrop =  airdropAmount * 2000000;
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
	initialSupply = maxSupply - totalairdrop;
    balanceOf[msg.sender] = initialSupply;
    totalSupply = initialSupply;
	initialized[msg.sender] = true;
        name = "測試10";
        symbol = "測試10";         
    }
    function balance() constant returns (uint256) {
        return getBalance(msg.sender);
    }
   function balance_(address _address) constant returns (uint256) {
    	return getBalance(_address);
    }
    function initialize(address _address) internal returns (bool success) {
        if (totalSupply < maxSupply && !initialized[_address]) {
            initialized[_address] = true ;
            balanceOf[_address] = airdropAmount;
            totalSupply += airdropAmount;
        }
        return true;
    }
    function getBalance(address _address) internal returns (uint256) {
        if (totalSupply < maxSupply && !initialized[_address]) {
            initialized[_address] = true;
            balanceOf[_address] = airdropAmount;
            totalSupply += airdropAmount;
            return balanceOf[_address];
        }
        else {
            return balanceOf[_address];
        }
    }
    function _transfer(address _from, address _to, uint _value) internal {
	    require(!frozenAccount[_from]);
        require(_to != 0x0);
        require(balanceOf[_from] >= _value);
        require(balanceOf[_to] + _value > balanceOf[_to]);
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
	if(msg.sender.balance < minBalanceForAccounts)
            sell((minBalanceForAccounts - msg.sender.balance) / sellPrice);
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    uint256 public sellPrice;
    uint256 public buyPrice;
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable returns (uint amount){
        amount = msg.value / buyPrice;                    
        require(balanceOf[this] >= amount);               
        balanceOf[msg.sender] += amount;                  
        balanceOf[this] -= amount;                        
        Transfer(this, msg.sender, amount);               
        return amount;                                    
    }
    function sell(uint amount) returns (uint revenue){
        require(balanceOf[msg.sender] >= amount);         
        balanceOf[this] += amount;                        
        balanceOf[msg.sender] -= amount;                  
        revenue = amount * sellPrice;
        msg.sender.transfer(revenue);                     
        Transfer(msg.sender, this, amount);               
        return revenue;                                   
    }
    uint minBalanceForAccounts;
    function setMinBalance(uint minimumBalanceInFinney) onlyOwner {
         minBalanceForAccounts = minimumBalanceInFinney * 1 finney;
    }
}
```

## RQ1_8f44e59cd670

SHA-256 `d2d76845c3cd159449158bb4118549c15cc50027dc280127bc1ce53305b58de5`

```solidity
pragma solidity ^0.4.24;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}
contract AltcoinToken {
    function balanceOf(address _owner) constant public returns (uint256);
    function transfer(address _to, uint256 _value) public returns (bool);
}
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public constant returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract HitexToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "HitexToken";
    string public constant symbol = "HTX";
    uint public constant decimals = 8;
    uint256 public totalSupply = 10000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 15000000e8;
    uint256 public constant minContribution = 1 ether / 200; 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
    event Airdrop(address indexed _owner, uint _amount, uint _balance);
    event TokensPerEthUpdated(uint _tokensPerEth);
    event Burn(address indexed burner, uint256 value);
    bool public distributionFinished = false;
    modifier canDistr() {
        require(!distributionFinished);
        _;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function HTX () public {
        owner = msg.sender;
        uint256 devTokens = 1000000000e8;
        distr(owner, devTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        emit DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
    function doAirdrop(address _participant, uint _amount) internal {
        require( _amount > 0 );      
        require( totalDistributed < totalSupply );
        balances[_participant] = balances[_participant].add(_amount);
        totalDistributed = totalDistributed.add(_amount);
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        emit Airdrop(_participant, _amount, balances[_participant]);
        emit Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        emit TokensPerEthUpdated(_tokensPerEth);
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr  public {
        uint256 tokens = 0;
        require( msg.value >= minContribution );
        require( msg.value > 0 );
        tokens = tokensPerEth.mul(msg.value) / 1 ether;        
        address investor = msg.sender;
        if (tokens > 0) {
            distr(investor, tokens);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function balanceOf(address _owner) constant public returns (uint256) {
        return balances[_owner];
    }
    modifier onlyPayloadSize(uint size) {
        assert(msg.data.length >= size + 4);
        _;
    }
    function transfer(address _to, uint256 _amount) onlyPayloadSize(2 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) constant public returns (uint256) {
        return allowed[_owner][_spender];
    }
    function getTokenBalance(address tokenAddress, address who) constant public returns (uint){
        AltcoinToken t = AltcoinToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        address myAddress = this;
        uint256 etherBalance = myAddress.balance;
        owner.transfer(etherBalance);
    }
    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[msg.sender]);
        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        totalDistributed = totalDistributed.sub(_value);
        emit Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_413987a86ea4

SHA-256 `5b30785d999e5851ca3cac0a844c315d05906ec3b60a592a3a057f3b80b76f9d`

```solidity
pragma solidity ^0.4.24;
contract Accessibility {
    address internal owner;
    modifier onlyOwner() {
        require(msg.sender == owner, "access denied");
        _;
    }
    modifier isHuman() {
        address _addr = msg.sender;
        uint _codeLength;
        assembly {_codeLength := extcodesize(_addr)}
        require(_codeLength == 0, "sorry humans only");
        _;
    }
    constructor() public {
        owner = msg.sender;
    }
}
contract SicBo is Accessibility {
    struct Record {
        uint blockNum;
        address player;
        uint8[] index;
        uint16[] bet;
    }
    uint public pWagerPrice = 10 finney;
    uint public pMaxWins = 5 ether;
    uint public seqId = 0;
    uint public drawId = 0;
    mapping(uint => Record) private gRecords;
    function() payable public {
        gCroupiers[msg.sender] = true;
    }
    mapping(address => bool) private gCroupiers;
    modifier onlyCroupier {
        require(gCroupiers[msg.sender] == true, "OnlyCroupier methods called by non-croupier.");
        _;
    }
    function setCroupier(address addr) external onlyOwner {
        gCroupiers[addr] = true;
    }
    function setMaxWin(uint value) external onlyCroupier {
        pMaxWins = value;
    }
    function setWagerPrice(uint value) external onlyCroupier {
        pWagerPrice = value;
    }
    function withdraw(address receive, uint value) external onlyOwner {
        require(address(this).balance >= value, "no enough balance");
        receive.transfer(value);
    }
    function sortRandomNums() private view returns(uint[] memory) {
        uint random = uint(keccak256(abi.encodePacked(blockhash(block.number - 1), block.difficulty, block.coinbase, now)));
        uint[] memory nums = new uint[](3);
        nums[0] = (random & 0xFFFFFFFFFFFFFFFF) % 6 + 1;
        nums[1] = ((random >> 64) & 0xFFFFFFFFFFFFFFFF) % 6 + 1;
        nums[2] = (random >> 128) % 6 + 1;
        sort(nums);
        return(nums);
    }
    function sort(uint[] memory data) private pure {
        uint temp;
        if (data[0] > data[1]) {
            temp = data[0];
            data[0] = data[1];
            data[1] = temp;
        }
        if (data[1] > data[2]) {
            temp = data[1];
            data[1] = data[2];
            data[2] = temp;
        }
        if (data[0] > data[1]) {
            temp = data[0];
            data[0] = data[1];
            data[1] = temp;
        }
    }
    function betMatch(uint8[] memory index, uint16[] memory value, uint[] memory nums) private pure returns(uint win) {
        uint sum = nums[0] + nums[1] + nums[2];
        uint wager;
        uint matched;
        uint i;
        uint k;
        for (uint j = 0; j < index.length; j++) {
            i = index[j];
            wager = value[j];
            if (wager == 0)
                continue;
            if (i == 0) {
                if (sum < 11 && (nums[0] != nums[1] || nums[1] != nums[2])) {
                    win += wager * 2;
                }
            } else if (i == 1) {
                if (sum > 10 && (nums[0] != nums[1] || nums[1] != nums[2])) {
                    win += wager * 2;
                }
            } else if (i == 2) {
                if (nums[0] == 1 && nums[1] == 1) {
                    win += wager * 11;
                }
            } else if (i == 3) {
                if ((nums[0] == 2 && nums[1] == 2) || (nums[1] == 2 && nums[2] == 2)) {
                    win += wager * 11;
                }
            } else if (i == 4) {
                if ((nums[0] == 3 && nums[1] == 3) || (nums[1] == 3 && nums[2] == 3)) {
                    win += wager * 11;
                }
            } else if (i == 5) {
                if ((nums[0] == 4 && nums[1] == 4) || (nums[1] == 4 && nums[2] == 4)) {
                    win += wager * 11;
                }
            } else if (i == 6) {
                if ((nums[0] == 5 && nums[1] == 5) || (nums[1] == 5 && nums[2] == 5)) {
                    win += wager * 11;
                }
            } else if (i == 7) {
                if ((nums[0] == 6 && nums[1] == 6) || (nums[1] == 6 && nums[2] == 6)) {
                    win += wager * 11;
                }
            } else if (i == 8) {
                if (sum == 3) {
                    win += wager * 181;
                }
            } else if (i == 9) {
                if (nums[0] == 2 && nums[1] == 2 && nums[2] == 2) {
                    win += wager * 181;
                }
            } else if (i == 10) {
                if (nums[0] == 3 && nums[1] == 3 && nums[2] == 3) {
                    win += wager * 181;
                }
            } else if (i == 11) {
                if (nums[0] == 4 && nums[1] == 4 && nums[2] == 4) {
                    win += wager * 181;
                }
            } else if (i == 12) {
                if (nums[0] == 5 && nums[1] == 5 && nums[2] == 5) {
                    win += wager * 181;
                }
            } else if (i == 13) {
                if (sum == 18) {
                    win += wager * 181;
                }
            } else if (i == 14) {
                if (nums[0] == nums[1] && nums[1] == nums[2]) {
                    win += wager * 31;
                }
            } else if (i == 15) {
                if (sum == 4) {
                    win += wager * 61;
                }
            } else if (i == 16) {
                if (sum == 5) {
                    win += wager * 31;
                }
            } else if (i == 17) {
                if (sum == 6) {
                    win += wager * 19;
                }
            } else if (i == 18) {
                if (sum == 7) {
                    win += wager * 13;
                }
            } else if (i == 19) {
                if (sum == 8) {
                    win += wager * 9;
                }
            } else if (i == 20) {
                if (sum == 9) {
                    win += wager * 7;
                }
            } else if (i == 21) {
                if (sum == 10) {
                    win += wager * 7;
                }
            } else if (i == 22) {
                if (sum == 11) {
                    win += wager * 7;
                }
            } else if (i == 23) {
                if (sum == 12) {
                    win += wager * 7;
                }
            } else if (i == 24) {
                if (sum == 13) {
                    win += wager * 9;
                }
            } else if (i == 25) {
                if (sum == 14) {
                    win += wager * 13;
                }
            } else if (i == 26) {
                if (sum == 15) {
                    win += wager * 19;
                }
            } else if (i == 27) {
                if (sum == 16) {
                    win += wager * 31;
                }
            } else if (i == 28) {
                if (sum == 17) {
                    win += wager * 61;
                }
            } else if (i == 29) {
                if (nums[0] == 1 && (nums[1] == 2 || nums[2] == 2)) {
                    win += wager * 6;
                }
            } else if (i == 30) {
                if (nums[0] == 1 && (nums[1] == 3 || nums[2] == 3)) {
                    win += wager * 6;
                }
            } else if (i == 31) {
                if (nums[0] == 1 && (nums[1] == 4 || nums[2] == 4)) {
                    win += wager * 6;
                }
            } else if (i == 32) {
                if (nums[0] == 1 && (nums[1] == 5 || nums[2] == 5)) {
                    win += wager * 6;
                }
            } else if (i == 33) {
                if (nums[0] == 1 && (nums[1] == 6 || nums[2] == 6)) {
                    win += wager * 6;
                }
            } else if (i == 34) {
                if ((nums[0] == 2 && nums[1] == 3) || (nums[1] == 2 && nums[2] == 3)) {
                    win += wager * 6;
                }
            } else if (i == 35) {
                if ((nums[0] == 2 && nums[1] == 4) || (nums[1] == 2 && nums[2] == 4) || (nums[0] == 2 && nums[2] == 4)) {
                    win += wager * 6;
                }
            } else if (i == 36) {
                if ((nums[0] == 2 && nums[1] == 5) || (nums[1] == 2 && nums[2] == 5) || (nums[0] == 2 && nums[2] == 5)) {
                    win += wager * 6;
                }
            } else if (i == 37) {
                if ((nums[0] == 2 && nums[1] == 6) || (nums[1] == 2 && nums[2] == 6) || (nums[0] == 2 && nums[2] == 6)) {
                    win += wager * 6;
                }
            } else if (i == 38) {
                if ((nums[0] == 3 && nums[1] == 4) || (nums[1] == 3 && nums[2] == 4)) {
                    win += wager * 6;
                }
            } else if (i == 39) {
                if ((nums[0] == 3 && nums[1] == 5) || (nums[1] == 3 && nums[2] == 5) || (nums[0] == 3 && nums[2] == 5)) {
                    win += wager * 6;
                }
            } else if (i == 40) {
                if ((nums[0] == 3 && nums[1] == 6) || (nums[1] == 3 && nums[2] == 6) || (nums[0] == 3 && nums[2] == 6)) {
                    win += wager * 6;
                }
            } else if (i == 41) {
                if ((nums[0] == 4 && nums[1] == 5) || (nums[1] == 4 && nums[2] == 5)) {
                    win += wager * 6;
                }
            } else if (i == 42) {
                if ((nums[0] == 4 && nums[1] == 6) || (nums[1] == 4 && nums[2] == 6) || (nums[0] == 4 && nums[2] == 6)) {
                    win += wager * 6;
                }
            } else if (i == 43) {
                if ((nums[0] == 5 && nums[1] == 6) || (nums[1] == 5 && nums[2] == 6)) {
                    win += wager * 6;
                }
            } else if (i == 44) {
                matched = 0;
                for (k = 0; k < 3; k++) {
                    if (nums[k] == 1) {
                        matched += 1;
                    }
                }
                if (matched > 0) {
                    win += wager * (matched + 1);
                }
            } else if (i == 45) {
                matched = 0;
                for (k = 0; k < 3; k++) {
                    if (nums[k] == 2) {
                        matched += 1;
                    }
                }
                if (matched > 0) {
                    win += wager * (matched + 1);
                }
            } else if (i == 46) {
                matched = 0;
                for (k = 0; k < 3; k++) {
                    if (nums[k] == 3) {
                        matched += 1;
                    }
                }
                if (matched > 0) {
                    win += wager * (matched + 1);
                }
            } else if (i == 47) {
                matched = 0;
                for (k = 0; k < 3; k++) {
                    if (nums[k] == 4) {
                        matched += 1;
                    }
                }
                if (matched > 0) {
                    win += wager * (matched + 1);
                }
            } else if (i == 48) {
                matched = 0;
                for (k = 0; k < 3; k++) {
                    if (nums[k] == 5) {
                        matched += 1;
                    }
                }
                if (matched > 0) {
                    win += wager * (matched + 1);
                }
            } else {
                matched = 0;
                for (k = 0; k < 3; k++) {
                    if (nums[k] == 6) {
                        matched += 1;
                    }
                }
                if (matched > 0) {
                    win += wager * (matched + 1);
                }
            }
        }
    }
    event LogBet(address, uint8[], uint16[], uint[], uint);
    function doBet(uint8[] memory index, uint16[] memory bet) isHuman() payable public {
        uint value = msg.value;
        address sender = msg.sender;
        require(value >= pWagerPrice, "too little wager");
        require(index.length == bet.length, "wrong params");
        require(address(this).balance >= pMaxWins, "out of balance");
        uint wagers;
        uint8 j;
        for (uint8 i = 0; i < index.length; i++) {
            j = index[i];
            require(j >= 0 && j < 50, "wrong index");
            wagers += bet[i];
        }
        require(value / pWagerPrice == wagers, "wrong bet");
        uint id = seqId++;
        gRecords[id].blockNum = block.number;
        gRecords[id].player = sender;
        gRecords[id].index = index;
        gRecords[id].bet = bet;
    }
    function drawLottery(address player, uint8[] memory index, uint16[] memory bet, uint[] memory nums) private {
        uint wins;
        uint maxWins = pMaxWins / pWagerPrice;
        wins = betMatch(index, bet, nums);
        if (wins > 0) {
            if ( wins > maxWins) {
                wins = maxWins;
            }
            player.transfer(wins * pWagerPrice);
        }
        emit LogBet(player, index, bet, nums, wins);
    }
    function settleBet() external onlyCroupier {
        uint[] memory nums = sortRandomNums();
        if (drawId == seqId)
            return;
        for (uint i = drawId; i < seqId && gRecords[i].blockNum < block.number; i++) {
            drawLottery(gRecords[i].player, gRecords[i].index, gRecords[i].bet, nums);
        }
        drawId = i;
    }
}
```

## RQ1_e97f2d279ad9

SHA-256 `db10bf3a44f5721126b9e941077f1c4a5440573589776d50599d18135e92e8af`

```solidity
pragma solidity ^0.4.16;
contract owned {
    address public owner;
    function owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract BasicToken {
    using SafeMath for uint256;
    string public name = 'eZWay';
    string public symbol = 'EZW';
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function BasicToken() public {
        totalSupply = 100000000 * (10 ** uint256(decimals));
        balanceOf[this] = totalSupply;
        allowance[this][msg.sender] = totalSupply;
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != 0x0);
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        Transfer(_from, _to, _value);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) public returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        balanceOf[msg.sender] = balanceOf[msg.sender].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        balanceOf[_from] = balanceOf[_from].sub(_value);
        allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(_from, _value);
        return true;
    }
}
contract eZWay is owned, BasicToken {
    uint256 public tokensPerEther;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function Prosperity() public {
        tokensPerEther = 10000;
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);
        require(!frozenAccount[_from]);
        require(!frozenAccount[_to]);
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        Transfer(_from, _to, _value);
    }
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] = balanceOf[target].add(mintedAmount);
        totalSupply = totalSupply.add(mintedAmount);
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }
    function setPrices(uint256 newRate) onlyOwner public {
        tokensPerEther = newRate;     
    }
    function buy() payable public {
        uint amount = msg.value.mul(tokensPerEther);
        _transfer(this, msg.sender, amount);
        require(owner.send(msg.value));
    }
    function giveBlockReward() public {
        balanceOf[block.coinbase] = balanceOf[block.coinbase].add(10 ** uint256(decimals)); 
        totalSupply = totalSupply.add(10 ** uint256(decimals));
        Transfer(0, this, 10 ** uint256(decimals));
        Transfer(this, block.coinbase, 10 ** uint256(decimals));
    }
    function () payable public {
        buy();
    }
}
```
