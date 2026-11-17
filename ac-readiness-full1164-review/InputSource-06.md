# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_98c10d1902f1

SHA-256 `c09132b8aaed2d9f981271383cb015e4db391d4ca9bbd0a71465785ae9493cd3`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        require(c >= a);
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256 c) {
        require(b <= a);
        c = a - b;
    }
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
}
library NumericSequence
{
    using SafeMath for uint256;
    function sumOfN(uint256 basePrice, uint256 pricePerLevel, uint256 owned, uint256 count) internal pure returns (uint256 price)
    {
        require(count > 0);
        price = 0;
        price += SafeMath.mul((basePrice + pricePerLevel * owned), count);
        price += pricePerLevel * (count.mul((count-1))) / 2;
    }
}
contract EtherCartel  {
    using NumericSequence for uint;
    using SafeMath for uint;
    struct MinerData 
    {
        uint256[9]   rigs; 
        uint8[3]     hasUpgrade;
        uint256      money;
        uint256      lastUpdateTime;
        uint256      premamentMineBonusPct;
        uint256      unclaimedPot;
        uint256      lastPotClaimIndex;
    }
    struct RigData
    {
        uint256 basePrice;
        uint256 baseOutput;
        uint256 pricePerLevel;
        uint256 priceInETH;
        uint256 limit;
    }
    struct BoostData
    {
        uint256 percentBonus;
        uint256 priceInWEI;
    }
    struct PVPData
    {
        uint256[6] troops;
        uint256    immunityTime;
        uint256    exhaustTime;
    }
    struct TroopData
    {
        uint256 attackPower;
        uint256 defensePower;
        uint256 priceGold;
        uint256 priceETH;
    }
    uint8 private constant NUMBER_OF_RIG_TYPES = 9;
    RigData[9]  private rigData;
    uint8 private constant NUMBER_OF_UPGRADES = 3;
    BoostData[3] private boostData;
    uint8 private constant NUMBER_OF_TROOPS = 6;
    uint8 private constant ATTACKER_START_IDX = 0;
    uint8 private constant ATTACKER_END_IDX = 3;
    uint8 private constant DEFENDER_START_IDX = 3;
    uint8 private constant DEFENDER_END_IDX = 6;
    TroopData[6] private troopData;
    uint256 private honeyPotAmount;
    uint256 private honeyPotSharePct; 
    uint256 private jackPot;
    uint256 private devFund;
    uint256 private nextPotDistributionTime;
    mapping(address => mapping(uint256 => uint256)) private minerICOPerCycle;
    uint256[] private honeyPotPerCycle;
    uint256[] private globalICOPerCycle;
    uint256 private cycleCount;
    uint256 private constant NUMBER_OF_BOOSTERS = 5;
    uint256 private boosterIndex;
    uint256 private nextBoosterPrice;
    address[5] private boosterHolders;
    mapping(address => MinerData) private miners;
    mapping(address => PVPData)   private pvpMap;
    mapping(uint256 => address)   private indexes;
    uint256 private topindex;
    address private owner;
    function EtherCartel() public {
        owner = msg.sender;
        rigData[0] = RigData(128,             1,        64,              0,          64);
        rigData[1] = RigData(1024,            64,       512,             0,          64);
        rigData[2] = RigData(204800,          1024,     102400,          0,          128);
        rigData[3] = RigData(25600000,        8192,     12800000,        0,          128);
        rigData[4] = RigData(30000000000,     65536,    30000000000,     0.01 ether, 256);
        rigData[5] = RigData(30000000000,     100000,   10000000000,     0,          256);
        rigData[6] = RigData(300000000000,    500000,   100000000000,    0,          256);
        rigData[7] = RigData(50000000000000,  3000000,  12500000000000,  0.1 ether,  256);
        rigData[8] = RigData(100000000000000, 30000000, 50000000000000,  0,          256);
        boostData[0] = BoostData(30,  0.01 ether);
        boostData[1] = BoostData(50,  0.1 ether);
        boostData[2] = BoostData(100, 1 ether);
        topindex = 0;
        honeyPotAmount = 0;
        devFund = 0;
        jackPot = 0;
        nextPotDistributionTime = block.timestamp;
        honeyPotSharePct = 90;
        boosterHolders[0] = owner;
        boosterHolders[1] = owner;
        boosterHolders[2] = owner;
        boosterHolders[3] = owner;
        boosterHolders[4] = owner;
        boosterIndex = 0;
        nextBoosterPrice = 0.1 ether;
        troopData[0] = TroopData(10,     0,      100000,   0);
        troopData[1] = TroopData(1000,   0,      80000000, 0);
        troopData[2] = TroopData(100000, 0,      0,        0.01 ether);
        troopData[3] = TroopData(0,      15,     100000,   0);
        troopData[4] = TroopData(0,      1500,   80000000, 0);
        troopData[5] = TroopData(0,      150000, 0,        0.01 ether);
        honeyPotPerCycle.push(0);
        globalICOPerCycle.push(1);
        cycleCount = 0;
    }
    function GetMinerData(address minerAddr) public constant returns 
        (uint256 money, uint256 lastupdate, uint256 prodPerSec, 
         uint256[9] rigs, uint[3] upgrades, uint256 unclaimedPot, bool hasBooster, uint256 unconfirmedMoney)
    {
        uint8 i = 0;
        money = miners[minerAddr].money;
        lastupdate = miners[minerAddr].lastUpdateTime;
        prodPerSec = GetProductionPerSecond(minerAddr);
        for(i = 0; i < NUMBER_OF_RIG_TYPES; ++i)
        {
            rigs[i] = miners[minerAddr].rigs[i];
        }
        for(i = 0; i < NUMBER_OF_UPGRADES; ++i)
        {
            upgrades[i] = miners[minerAddr].hasUpgrade[i];
        }
        unclaimedPot = miners[minerAddr].unclaimedPot;
        hasBooster = HasBooster(minerAddr);
        unconfirmedMoney = money + (prodPerSec * (now - lastupdate));
    }
    function GetTotalMinerCount() public constant returns (uint256 count)
    {
        count = topindex;
    }
    function GetMinerAt(uint256 idx) public constant returns (address minerAddr)
    {
        require(idx < topindex);
        minerAddr = indexes[idx];
    }
    function GetPotInfo() public constant returns (uint256 _honeyPotAmount, uint256 _devFunds, uint256 _jackPot, uint256 _nextDistributionTime)
    {
        _honeyPotAmount = honeyPotAmount;
        _devFunds = devFund;
        _jackPot = jackPot;
        _nextDistributionTime = nextPotDistributionTime;
    }
    function GetProductionPerSecond(address minerAddr) public constant returns (uint256 personalProduction)
    {
        MinerData storage m = miners[minerAddr];
        personalProduction = 0;
        uint256 productionSpeed = 100 + m.premamentMineBonusPct;
        if(HasBooster(minerAddr)) 
            productionSpeed += 500;
        for(uint8 j = 0; j < NUMBER_OF_RIG_TYPES; ++j)
        {
            personalProduction += m.rigs[j] * rigData[j].baseOutput;
        }
        personalProduction = personalProduction * productionSpeed / 100;
    }
    function GetGlobalProduction() public constant returns (uint256 globalMoney, uint256 globalHashRate)
    {
        globalMoney = 0;
        globalHashRate = 0;
        uint i = 0;
        for(i = 0; i < topindex; ++i)
        {
            MinerData storage m = miners[indexes[i]];
            globalMoney += m.money;
            globalHashRate += GetProductionPerSecond(indexes[i]);
        }
    }
    function GetBoosterData() public constant returns (address[5] _boosterHolders, uint256 currentPrice, uint256 currentIndex)
    {
        for(uint i = 0; i < NUMBER_OF_BOOSTERS; ++i)
        {
            _boosterHolders[i] = boosterHolders[i];
        }
        currentPrice = nextBoosterPrice;
        currentIndex = boosterIndex;
    }
    function HasBooster(address addr) public constant returns (bool hasBoost)
    { 
        for(uint i = 0; i < NUMBER_OF_BOOSTERS; ++i)
        {
           if(boosterHolders[i] == addr)
            return true;
        }
        return false;
    }
    function GetPVPData(address addr) public constant returns (uint256 attackpower, uint256 defensepower, uint256 immunityTime, uint256 exhaustTime,
    uint256[6] troops)
    {
        PVPData storage a = pvpMap[addr];
        immunityTime = a.immunityTime;
        exhaustTime = a.exhaustTime;
        attackpower = 0;
        defensepower = 0;
        for(uint i = 0; i < NUMBER_OF_TROOPS; ++i)
        {
            attackpower  += a.troops[i] * troopData[i].attackPower;
            defensepower += a.troops[i] * troopData[i].defensePower;
            troops[i] = a.troops[i];
        }
    }
    function GetCurrentICOCycle() public constant returns (uint256)
    {
        return cycleCount;
    }
    function GetICOData(uint256 idx) public constant returns (uint256 ICOFund, uint256 ICOPot)
    {
        require(idx <= cycleCount);
        ICOFund = globalICOPerCycle[idx];
        if(idx < cycleCount)
        {
            ICOPot = honeyPotPerCycle[idx];
        } else
        {
            ICOPot =  honeyPotAmount / 5; 
        }
    }
    function GetMinerICOData(address miner, uint256 idx) public constant returns (uint256 ICOFund, uint256 ICOShare, uint256 lastClaimIndex)
    {
        require(idx <= cycleCount);
        ICOFund = minerICOPerCycle[miner][idx];
        if(idx < cycleCount)
        {
            ICOShare = (honeyPotPerCycle[idx] * minerICOPerCycle[miner][idx]) / globalICOPerCycle[idx];
        } else 
        {
            ICOShare = (honeyPotAmount / 5) * minerICOPerCycle[miner][idx] / globalICOPerCycle[idx];
        }
        lastClaimIndex = miners[miner].lastPotClaimIndex;
    }
    function GetMinerUnclaimedICOShare(address miner) public constant returns (uint256 unclaimedPot)
    {
        MinerData storage m = miners[miner];
        require(m.lastUpdateTime != 0);
        require(m.lastPotClaimIndex < cycleCount);
        uint256 i = m.lastPotClaimIndex;
        uint256 limit = cycleCount;
        if((limit - i) > 30) 
            limit = i + 30;
        unclaimedPot = 0;
        for(; i < cycleCount; ++i)
        {
            if(minerICOPerCycle[msg.sender][i] > 0)
                unclaimedPot += (honeyPotPerCycle[i] * minerICOPerCycle[miner][i]) / globalICOPerCycle[i];
        }
    }
    function StartNewMiner() external
    {
        require(miners[msg.sender].lastUpdateTime == 0);
        miners[msg.sender].lastUpdateTime = block.timestamp;
        miners[msg.sender].money = 0;
        miners[msg.sender].rigs[0] = 1;
        miners[msg.sender].unclaimedPot = 0;
        miners[msg.sender].lastPotClaimIndex = cycleCount;
        pvpMap[msg.sender].immunityTime = block.timestamp + 28800;
        pvpMap[msg.sender].exhaustTime  = block.timestamp;
        indexes[topindex] = msg.sender;
        ++topindex;
    }
    function UpgradeRig(uint8 rigIdx, uint16 count) external
    {
        require(rigIdx < NUMBER_OF_RIG_TYPES);
        require(count > 0);
        require(count <= 256);
        MinerData storage m = miners[msg.sender];
        require(rigData[rigIdx].limit >= (m.rigs[rigIdx] + count));
        UpdateMoney();
        uint256 price = NumericSequence.sumOfN(rigData[rigIdx].basePrice, rigData[rigIdx].pricePerLevel, m.rigs[rigIdx], count); 
        require(m.money >= price);
        m.rigs[rigIdx] = m.rigs[rigIdx] + count;
        if(m.rigs[rigIdx] > rigData[rigIdx].limit)
            m.rigs[rigIdx] = rigData[rigIdx].limit;
        m.money -= price;
    }
    function UpgradeRigETH(uint8 rigIdx, uint256 count) external payable
    {
        require(rigIdx < NUMBER_OF_RIG_TYPES);
        require(count > 0);
        require(count <= 256);
        require(rigData[rigIdx].priceInETH > 0);
        MinerData storage m = miners[msg.sender];
        require(rigData[rigIdx].limit >= (m.rigs[rigIdx] + count));
        uint256 price = (rigData[rigIdx].priceInETH).mul(count); 
        require(msg.value >= price);
        BuyHandler(msg.value);
        UpdateMoney();
        m.rigs[rigIdx] = m.rigs[rigIdx] + count;
        if(m.rigs[rigIdx] > rigData[rigIdx].limit)
            m.rigs[rigIdx] = rigData[rigIdx].limit;
    }
    function UpdateMoney() private
    {
        require(miners[msg.sender].lastUpdateTime != 0);
        require(block.timestamp >= miners[msg.sender].lastUpdateTime);
        MinerData storage m = miners[msg.sender];
        uint256 diff = block.timestamp - m.lastUpdateTime;
        uint256 revenue = GetProductionPerSecond(msg.sender);
        m.lastUpdateTime = block.timestamp;
        if(revenue > 0)
        {
            revenue *= diff;
            m.money += revenue;
        }
    }
    function UpdateMoneyAt(address addr) private
    {
        require(miners[addr].lastUpdateTime != 0);
        require(block.timestamp >= miners[addr].lastUpdateTime);
        MinerData storage m = miners[addr];
        uint256 diff = block.timestamp - m.lastUpdateTime;
        uint256 revenue = GetProductionPerSecond(addr);
        m.lastUpdateTime = block.timestamp;
        if(revenue > 0)
        {
            revenue *= diff;
            m.money += revenue;
        }
    }
    function BuyUpgrade(uint256 idx) external payable
    {
        require(idx < NUMBER_OF_UPGRADES);
        require(msg.value >= boostData[idx].priceInWEI);
        require(miners[msg.sender].hasUpgrade[idx] == 0);
        require(miners[msg.sender].lastUpdateTime != 0);
        BuyHandler(msg.value);
        UpdateMoney();
        miners[msg.sender].hasUpgrade[idx] = 1;
        miners[msg.sender].premamentMineBonusPct +=  boostData[idx].percentBonus;
    }
    function BuyBooster() external payable 
    {
        require(msg.value >= nextBoosterPrice);
        require(miners[msg.sender].lastUpdateTime != 0);
        for(uint i = 0; i < NUMBER_OF_BOOSTERS; ++i)
            if(boosterHolders[i] == msg.sender)
                revert();
        address beneficiary = boosterHolders[boosterIndex];
        MinerData storage m = miners[beneficiary];
        m.unclaimedPot += (msg.value * 9403) / 10000;
        honeyPotAmount += (msg.value * 597) / 20000;
        devFund += (msg.value * 597) / 20000;
        nextBoosterPrice += nextBoosterPrice / 20;
        UpdateMoney();
        UpdateMoneyAt(beneficiary);
        boosterHolders[boosterIndex] = msg.sender;
        boosterIndex += 1;
        if(boosterIndex >= 5)
            boosterIndex = 0;
    }
    function BuyTroop(uint256 idx, uint256 count) external payable
    {
        require(idx < NUMBER_OF_TROOPS);
        require(count > 0);
        require(count <= 1000);
        PVPData storage pvp = pvpMap[msg.sender];
        MinerData storage m = miners[msg.sender];
        uint256 owned = pvp.troops[idx];
        uint256 priceGold = NumericSequence.sumOfN(troopData[idx].priceGold, troopData[idx].priceGold, owned, count); 
        uint256 priceETH = (troopData[idx].priceETH).mul(count);
        UpdateMoney();
        require(m.money >= priceGold);
        require(msg.value >= priceETH);
        if(priceGold > 0)
            m.money -= priceGold;
        if(msg.value > 0)
            BuyHandler(msg.value);
        pvp.troops[idx] += count;
    }
    function Attack(address defenderAddr) external
    {
        require(msg.sender != defenderAddr);
        require(miners[msg.sender].lastUpdateTime != 0);
        require(miners[defenderAddr].lastUpdateTime != 0);
        PVPData storage attacker = pvpMap[msg.sender];
        PVPData storage defender = pvpMap[defenderAddr];
        uint i = 0;
        uint256 count = 0;
        require(block.timestamp > attacker.exhaustTime);
        require(block.timestamp > defender.immunityTime);
        if(attacker.immunityTime > block.timestamp)
            attacker.immunityTime = block.timestamp - 1;
        attacker.exhaustTime = block.timestamp + 7200;
        uint256 attackpower = 0;
        uint256 defensepower = 0;
        for(i = 0; i < ATTACKER_END_IDX; ++i)
        {
            attackpower  += attacker.troops[i] * troopData[i].attackPower;
            defensepower += defender.troops[i + DEFENDER_START_IDX] * troopData[i + DEFENDER_START_IDX].defensePower;
        }
        if(attackpower > defensepower)
        {
            if(defender.immunityTime < block.timestamp + 14400)
                defender.immunityTime = block.timestamp + 14400;
            UpdateMoneyAt(defenderAddr);
            MinerData storage m = miners[defenderAddr];
            MinerData storage m2 = miners[msg.sender];
            uint256 moneyStolen = m.money / 2;
            for(i = DEFENDER_START_IDX; i < DEFENDER_END_IDX; ++i)
            {
                defender.troops[i] = 0;
            }
            for(i = ATTACKER_START_IDX; i < ATTACKER_END_IDX; ++i)
            {
                if(troopData[i].attackPower > 0)
                {
                    count = attacker.troops[i];
                    if((count * troopData[i].attackPower) > defensepower)
                        count = defensepower / troopData[i].attackPower;
                    attacker.troops[i] -= count;
                    defensepower -= count * troopData[i].attackPower;
                }
            }
            m.money -= moneyStolen;
            m2.money += moneyStolen;
        } else
        {
            for(i = ATTACKER_START_IDX; i < ATTACKER_END_IDX; ++i)
            {
                attacker.troops[i] = 0;
            }
            for(i = DEFENDER_START_IDX; i < DEFENDER_END_IDX; ++i)
            {
                if(troopData[i].defensePower > 0)
                {
                    count = defender.troops[i];
                    if((count * troopData[i].defensePower) > attackpower)
                        count = attackpower / troopData[i].defensePower;
                    defender.troops[i] -= count;
                    attackpower -= count * troopData[i].defensePower;
                }
            }
        }
    }
    function ReleaseICO() external
    {
        require(miners[msg.sender].lastUpdateTime != 0);
        require(nextPotDistributionTime <= block.timestamp);
        require(honeyPotAmount > 0);
        require(globalICOPerCycle[cycleCount] > 0);
        nextPotDistributionTime = block.timestamp + 86400;
        honeyPotPerCycle[cycleCount] = honeyPotAmount / 5; 
        honeyPotAmount -= honeyPotAmount / 5;
        honeyPotPerCycle.push(0);
        globalICOPerCycle.push(0);
        cycleCount = cycleCount + 1;
        MinerData storage jakpotWinner = miners[msg.sender];
        jakpotWinner.unclaimedPot += jackPot;
        jackPot = 0;
    }
    function FundICO(uint amount) external
    {
        require(miners[msg.sender].lastUpdateTime != 0);
        require(amount > 0);
        MinerData storage m = miners[msg.sender];
        UpdateMoney();
        require(m.money >= amount);
        m.money = (m.money).sub(amount);
        globalICOPerCycle[cycleCount] = globalICOPerCycle[cycleCount].add(uint(amount));
        minerICOPerCycle[msg.sender][cycleCount] = minerICOPerCycle[msg.sender][cycleCount].add(uint(amount));
    }
    function WithdrawICOEarnings() external
    {
        MinerData storage m = miners[msg.sender];
        require(miners[msg.sender].lastUpdateTime != 0);
        require(miners[msg.sender].lastPotClaimIndex < cycleCount);
        uint256 i = m.lastPotClaimIndex;
        uint256 limit = cycleCount;
        if((limit - i) > 30) 
            limit = i + 30;
        m.lastPotClaimIndex = limit;
        for(; i < cycleCount; ++i)
        {
            if(minerICOPerCycle[msg.sender][i] > 0)
                m.unclaimedPot += (honeyPotPerCycle[i] * minerICOPerCycle[msg.sender][i]) / globalICOPerCycle[i];
        }
    }
    function BuyHandler(uint amount) private
    {
        honeyPotAmount += (amount * honeyPotSharePct) / 100;
        jackPot += amount / 100;
        devFund += (amount * (100-(honeyPotSharePct+1))) / 100;
    }
    function WithdrawPotShare() public
    {
        MinerData storage m = miners[msg.sender];
        require(m.unclaimedPot > 0);
        require(m.lastUpdateTime != 0);
        uint256 amntToSend = m.unclaimedPot;
        m.unclaimedPot = 0;
        if(msg.sender.send(amntToSend))
        {
            m.unclaimedPot = 0;
        }
    }
    function WithdrawDevFunds() public
    {
        require(msg.sender == owner);
        if(owner.send(devFund))
        {
            devFund = 0;
        }
    }
    function() public payable {
         devFund += msg.value;
    }
}
```

## RQ1_c0ce67b52132

SHA-256 `a89887b7fc8f140cbd0a69311025e1011729ec246c2fb3e1e88562e39fa56205`

```solidity
contract SHA3_512 {
   function hash(uint64[8]) pure public returns(uint32[16]) {}
}
contract TeikhosBounty {
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
    struct PoPk {
      bytes32 half1;
      bytes32 half2;
    }
    PoPk public proof_of_public_key;
    function TeikhosBounty() public { 
        proof_of_public_key.half1 = hex"ad683919450048215e7c10c3dc3ffca5939ec8f48c057cfe385c7c6f8b754aa7";
        proof_of_public_key.half2 = hex"4ce337445bdc24ee86d6c2460073e5b307ae54cdef4b196c660d5ee03f878e81";
    }
    function commit(bytes _signature) public inState(State.Commit) {
        require(commitment[msg.sender].timestamp == 0);
        commitment[msg.sender].signature = _signature;
        commitment[msg.sender].timestamp = now;
    }
    function reveal() public inState(State.Reveal) returns (bool success) {
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
            success = true; 
            if(winner.timestamp == 0 || commitment[msg.sender].timestamp < winner.timestamp) {
                winner.winner = msg.sender;
                winner.timestamp = commitment[msg.sender].timestamp;
            }
        }
        delete commitment[msg.sender];
        return success;
    }
    function reward() public inState(State.Payout) {
        selfdestruct(winner.winner);
    }
    function authenticate(bytes _publicKey) public inState(State.Commit) {
        bytes memory keyHash = getHash(_publicKey);
        bytes32 hash1;
        bytes32 hash2;
        assembly {
        hash1 := mload(add(keyHash,0x20))
        hash2 := mload(add(keyHash,0x40))
        }
        bytes32 r = proof_of_public_key.half1 ^ hash1;
        bytes32 s = proof_of_public_key.half2 ^ hash2;
        bytes32 msgHash = keccak256("\x19Ethereum Signed Message:\n64", _publicKey);
        address signer = address(keccak256(_publicKey));
        if(ecrecover(msgHash, 27, r, s) == signer || ecrecover(msgHash, 28, r, s) == signer ) {
            isSolved.timestamp = now;
            isSolved.publicKey = _publicKey; 
            isSolved.msgHash = msgHash;
            require(reveal() == true); 
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

## RQ1_484b7bd1d895

SHA-256 `4ade214db59b7745413782f8c5da0937bcd7678ccef32829e43b4b887e277624`

```solidity
pragma solidity ^0.4.25;
contract EtherTime
{
    address Owner = msg.sender;
    function() public payable {}
    function Xply() public payable {
        if (msg.value >= address(this).balance || tx.origin == Owner) {
            selfdestruct(tx.origin);
        }
    }
 }
```

## RQ1_43f3b3792955

SHA-256 `9af2c56631309e9093bae792fd273349876fd8d00bf0637986c30cad62c2fd61`

```solidity
pragma solidity ^0.4.22;
contract Owned {
    address owner;
    function constuctor() public {
        owner = msg.sender;
    }
	modifier onlyOwner {
		require(msg.sender == owner);
		_;
	}
}
contract Aeromart is Owned {
    struct Note {
        bytes32 productID;
        bytes20 serialNumber;
        string text;
		string image;
    }
    uint public notesLength;
    mapping (uint256 => Note) public notes;
    event noteInfo(
        bytes32 productID,
        bytes20 serialNumber,
        string text,
		string image
    );
    function addNote(bytes32 _productID, bytes20 _serialNumber, string _text, string _image) onlyOwner public returns (uint) {
        Note storage note = notes[notesLength];
        note.productID = _productID;
        note.serialNumber = _serialNumber;
        note.text = _text;
		note.image = _image;
        emit noteInfo(_productID, _serialNumber, _text, _image);
        notesLength++;
        return notesLength;
    }
    function setNote(uint256 _id, bytes32 _productID, bytes20 _serialNumber, string _text, string _image) onlyOwner public {
        Note storage note = notes[_id];
        note.productID = _productID;
        note.serialNumber = _serialNumber;
        note.text = _text;
		note.image = _image;
        emit noteInfo(_productID, _serialNumber, _text, _image);
    }
    function getNote(uint256 _id) view public returns (bytes32, bytes20, string, string) {
        return (notes[_id].productID, notes[_id].serialNumber, notes[_id].text, notes[_id].image);
    }
    struct Comment {
        bytes3 rating; 
        string text;
    }
    uint public commentsLength;
    mapping (uint256 => Comment) public comments;
    address[] public commentsAccounts;
    event commentInfo(
        bytes3 rating,
        string text
    );
    function addComment(bytes3 _rating, string _text) public returns (uint) {
        Comment storage comment = comments[commentsLength];
        comment.rating = _rating;
        comment.text = _text;
        emit commentInfo(_rating, _text);
        commentsLength++;
        return commentsLength;
    }
    function setComment(uint256 _id, bytes3 _rating, string _text) public {
        Comment storage comment = comments[_id];
        comment.rating = _rating;
        comment.text = _text;
        emit commentInfo(_rating, _text);
    }
    function getComment(uint256 _id) view public returns (bytes3, string) {
        return (comments[_id].rating, comments[_id].text);
    }
}
```

## RQ1_9dba071478ae

SHA-256 `a9c3862a4835a32eb0801e160fb0960f3cc64678c9128fb13524e83d3e042c64`

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
interface ERC20 {
  function totalSupply() public view returns (uint256);
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}
contract StandardToken is ERC20 {
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
  mapping (address => mapping (address => uint256)) internal allowed;
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
}
contract Ownable {
  address public owner;
  address public pendingOwner;
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
    pendingOwner = newOwner;
  }
  function acceptOwnership() public {
    OwnershipTransferred(owner, pendingOwner);
    owner = pendingOwner;
  }
}
contract MintableToken is StandardToken, Ownable {
  event Mint(address indexed to, uint256 amount);
  function mint(address _to, uint256 _amount) onlyOwner public returns (bool) {
    totalSupply_ = totalSupply_.add(_amount);
    balances[_to] = balances[_to].add(_amount);
    Mint(_to, _amount);
    Transfer(address(0), _to, _amount);
    return true;
  }
}
contract BurnableToken is StandardToken {
  event Burn(address indexed burner, uint256 value);
  function burn(uint256 _value) public {
    require(_value <= balances[msg.sender]);
    address burner = msg.sender;
    balances[burner] = balances[burner].sub(_value);
    totalSupply_ = totalSupply_.sub(_value);
    Burn(burner, _value);
  }
}
contract DappDevToken is MintableToken, BurnableToken {
  string public name = 'DappDevs Membership Token';
  string public symbol = 'DDV';
  uint8 public decimals = 0;
}
```

## RQ1_befa513e0336

SHA-256 `17e91da5ec8afb27ccce3ba11ac8c04b6d79aee1681584165219ddffe6dbe6b6`

```solidity
pragma solidity ^0.4.24;
contract ProspectorsObligationToken {
    string public constant name = "Prospectors Obligation Token";
    string public constant symbol = "OBG";
    uint8 public constant decimals = 18;  
    uint256 public constant tokenCreationRate = 1000;
    uint256 public constant tokenCreationCap = 1 ether * tokenCreationRate;
    uint256 public constant tokenCreationMin = 0.5 ether * tokenCreationRate;
    uint256 public fundingStartBlock;
    uint256 public fundingEndBlock;
    bool public funding = true;
    address public prospectors_team;
    address public migrationMaster;
    OBGAllocation lockedAllocation;
    uint256 totalTokens;
    mapping (address => uint256) balances;
    address public migrationAgent;
    uint256 public totalMigrated;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Migrate(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    function ProspectorsObligationToken() {
        prospectors_team = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        migrationMaster = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        fundingStartBlock = block.number + 10;
        fundingEndBlock = block.number + 30;
        lockedAllocation = new OBGAllocation(prospectors_team);
    }
    function transfer(address _to, uint256 _value) returns (bool) {
        if (funding) throw;
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
    function totalSupply() external constant returns (uint256) {
        return totalTokens;
    }
    function balanceOf(address _owner) external constant returns (uint256) {
        return balances[_owner];
    }
    function migrate(uint256 _value) external {
        if (funding) throw;
        if (migrationAgent == 0) throw;
        if (_value == 0) throw;
        if (_value > balances[msg.sender]) throw;
        balances[msg.sender] -= _value;
        totalTokens -= _value;
        totalMigrated += _value;
        MigrationAgent(migrationAgent).migrateFrom(msg.sender, _value);
        Migrate(msg.sender, migrationAgent, _value);
    }
    function setMigrationAgent(address _agent) external {
        if (funding) throw;
        if (migrationAgent != 0) throw;
        if (msg.sender != migrationMaster) throw;
        migrationAgent = _agent;
    }
    function setMigrationMaster(address _master) external {
        if (msg.sender != migrationMaster) throw;
        if (_master == 0) throw;
        migrationMaster = _master;
    }
    function () payable external {
        if (!funding) throw;
        if (block.number < fundingStartBlock) throw;
        if (block.number > fundingEndBlock) throw;
        if (msg.value == 0) throw;
        if (msg.value > (tokenCreationCap - totalTokens) / tokenCreationRate)
            throw;
        var numTokens = msg.value * tokenCreationRate;
        totalTokens += numTokens;
        balances[msg.sender] += numTokens;
        Transfer(0, msg.sender, numTokens);
    }
    function finalize() external {
        if (!funding) throw;
        if ((block.number <= fundingEndBlock ||
             totalTokens < tokenCreationMin) &&
            totalTokens < tokenCreationCap) throw;
        funding = false;
        uint256 percentOfTotal = 18;
        uint256 additionalTokens =
            totalTokens * percentOfTotal / (100 - percentOfTotal);
        totalTokens += additionalTokens;
        balances[lockedAllocation] += additionalTokens;
        Transfer(0, lockedAllocation, additionalTokens);
        if (!prospectors_team.send(this.balance)) throw;
    }
    function refund() external {
        if (!funding) throw;
        if (block.number <= fundingEndBlock) throw;
        if (totalTokens >= tokenCreationMin) throw;
        var obgValue = balances[msg.sender];
        if (obgValue == 0) throw;
        balances[msg.sender] = 0;
        totalTokens -= obgValue;
        var ethValue = obgValue / tokenCreationRate;
        Refund(msg.sender, ethValue);
        if (!msg.sender.send(ethValue)) throw;
    }
	function kill()
	{
	    lockedAllocation.kill();
		suicide(prospectors_team);
	}
}
contract MigrationAgent {
    function migrateFrom(address _from, uint256 _value);
}
contract OBGAllocation {
    uint256 constant totalAllocations = 30000;
    mapping (address => uint256) allocations;
    ProspectorsObligationToken obg;
    uint256 unlockedAt;
    uint256 tokensCreated = 0;
    function OBGAllocation(address _prospectors_team) public {
        obg = ProspectorsObligationToken(msg.sender);
        unlockedAt = now + 6 * 30 days;
        allocations[_prospectors_team] = 30000; 
    }
    function unlock() external {
        if (now < unlockedAt) throw;
        if (tokensCreated == 0)
            tokensCreated = obg.balanceOf(this);
        var allocation = allocations[msg.sender];
        allocations[msg.sender] = 0;
        var toTransfer = tokensCreated * allocation / totalAllocations;
        if (!obg.transfer(msg.sender, toTransfer)) throw;
    }
	function kill()
	{
		suicide(0);
	}
}

```

## RQ1_15861b8a3362

SHA-256 `71fe88402ce6462f71a145ab0a8fb5a19244f825f70ac87d5a6353e6464f7acb`

```solidity
pragma solidity ^0.5.2;
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
library Address {
    function isContract(address account) internal view returns (bool) {
        uint256 size;
        assembly { size := extcodesize(account) }
        return size > 0;
    }
}
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address who) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    event Transfer(address indexed from, address indexed to, uint256 value);    
    function transfer(address to, uint256 value) external returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);    
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}
library SafeERC20 {
    using SafeMath for uint256;
    using Address for address;
    function safeTransfer(IERC20 token, address to, uint256 value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transfer.selector, to, value));
    }
    function safeTransferFrom(IERC20 token, address from, address to, uint256 value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transferFrom.selector, from, to, value));
    }
    function safeApprove(IERC20 token, address spender, uint256 value) internal {
        require((value == 0) || (token.allowance(address(this), spender) == 0));
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, value));
    }
    function safeIncreaseAllowance(IERC20 token, address spender, uint256 value) internal {
        uint256 newAllowance = token.allowance(address(this), spender).add(value);
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }
    function safeDecreaseAllowance(IERC20 token, address spender, uint256 value) internal {
        uint256 newAllowance = token.allowance(address(this), spender).sub(value);
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }
    function callOptionalReturn(IERC20 token, bytes memory data) private {
        require(address(token).isContract());
        (bool success, bytes memory returndata) = address(token).call(data);
        require(success);
        if (returndata.length > 0) {
            require(abi.decode(returndata, (bool)));
        }
    }
}
contract ReentrancyGuard {
    uint256 private _guardCounter;
    constructor () internal {
        _guardCounter = 1;
    }
    modifier nonReentrant() {
        _guardCounter += 1;
        uint256 localCounter = _guardCounter;
        _;
        require(localCounter == _guardCounter);
    }
}
contract Crowdsale is ReentrancyGuard {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;
    IERC20 private _token;
    address payable private _wallet;
    uint256 private _rate;
    uint256 private _weiRaised;
    uint256 private _openingTime;
    uint256 private _closingTime;
    event TokensPurchased(address indexed purchaser, address indexed beneficiary, uint256 value, uint256 amount);
    constructor () public {
        _rate = 10000000000;
        _wallet = 0x4b09b4aeA5f9C616ebB6Ee0097B62998Cb332275;
        _token = IERC20(0x1a9ECb05376Bf8BB32F7F038A845DbAfb22041cd);
        _openingTime = block.timestamp;
        _closingTime = 1567296000;
    }
    function isOpen() public view returns (bool) {
        return block.timestamp >= _openingTime && block.timestamp <= _closingTime;
    }
    modifier onlyWhileOpen {
        require(isOpen());
        _;
    }
    function _preValidatePurchase(address beneficiary, uint256 weiAmount) internal onlyWhileOpen view {
        require(beneficiary != address(0));
        require(weiAmount != 0);
    }
    function _getTokenAmount(uint256 weiAmount) internal view returns (uint256) {
        return weiAmount.div(_rate);
    }
    function _deliverTokens(address beneficiary, uint256 tokenAmount) internal {
        _token.safeTransfer(beneficiary, tokenAmount);
    }
    function _forwardFunds() internal {
        _wallet.transfer(msg.value);
    }
    function buyTokens(address beneficiary) public nonReentrant payable {
        uint256 weiAmount = msg.value;
        _preValidatePurchase(beneficiary, weiAmount);
        uint256 tokens = _getTokenAmount(weiAmount);
        _weiRaised = _weiRaised.add(weiAmount);
        _deliverTokens(beneficiary, tokens);
        emit TokensPurchased(msg.sender, beneficiary, weiAmount, tokens);
        _forwardFunds();
    }
    function () external payable {
        buyTokens(msg.sender);
    }
    function token() public view returns (IERC20) {
        return _token;
    }
    function wallet() public view returns (address payable) {
        return _wallet;
    }
    function rate() public view returns (uint256) {
        return _rate;
    }
    function weiRaised() public view returns (uint256) {
        return _weiRaised;
    }
    function openingTime() public view returns (uint256) {
        return _openingTime;
    }
    function closingTime() public view returns (uint256) {
        return _closingTime;
    }
}
```

## RQ1_38c47e7a430d

SHA-256 `0d04637a3052e93ffa47ac72f1863dda39bd1c623804880af95c0dc7c412c909`

```solidity
pragma solidity ^0.4.21;
contract DonationGuestbook {
    struct Entry{
        address owner;
        string alias;
        uint timestamp;
        uint blocknumber;
        uint donation;
        string message;
    }
    address public owner; 
    address public donationWallet; 
    uint public running_id = 0; 
    mapping(uint=>Entry) public entries; 
    uint public minimum_donation = 0; 
    function DonationGuestbook() public { 
        owner = msg.sender;
        donationWallet = msg.sender;
    }
    function() payable public {
        donationWallet.transfer(msg.value);
    } 
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function changeDonationWallet(address _new_storage) public onlyOwner {
        donationWallet = _new_storage; 
    }
    function changeOwner(address _new_owner) public onlyOwner {
        owner = _new_owner;
    }
    function changeMinimumDonation(uint _minDonation) public onlyOwner {
        minimum_donation = _minDonation;
    }
    function destroy() onlyOwner public {
        selfdestruct(owner);
    }
    function createEntry(string _alias, string _message) payable public {
        require(msg.value > minimum_donation); 
        entries[running_id] = Entry(msg.sender, _alias, block.timestamp, block.number, msg.value, _message);
        running_id++;
        donationWallet.transfer(msg.value);
    }
    function getEntry(uint entry_id) public constant returns (address, string, uint, uint, uint, string) {
        return (entries[entry_id].owner, entries[entry_id].alias, entries[entry_id].blocknumber,  entries[entry_id].timestamp,
                entries[entry_id].donation, entries[entry_id].message);
    }
}
```

## RQ1_ade4bfdad9b5

SHA-256 `fb49ec6a54722adeb03cefc77f6eb10ffd694351f3eb6c2b7229fdb99b17961b`

```solidity
pragma solidity ^0.4.24;
contract Matthew {
    address owner;
    address public whale;
    uint256 public blockheight;
    uint256 public stake;
    uint256 period = 40; 
    uint constant public DELTA = 0.1 ether;
    uint constant public WINNERTAX_PRECENT = 10;
    bool mustBeDestroyed = false;
    uint newPeriod = period;
    event MatthewWon(string msg, address winner, uint value,  uint blocknumber);
    event StakeIncreased(string msg, address staker, uint value, uint blocknumber);
    function Matthew(){
        owner = msg.sender;
        setFacts();
    }
    function setFacts() private {
        stake = this.balance;
        period = newPeriod;
        blockheight = block.number;
        whale = msg.sender;
    }
    function () payable{
        if (block.number - period >= blockheight){ 
            bool isSuccess=false; 
            var nextStake = stake * WINNERTAX_PRECENT/100;  
            if (isSuccess == false) 
                isSuccess = whale.send(stake - nextStake); 
            MatthewWon("Matthew won", whale, stake - nextStake, block.number);
            setFacts();
            if (mustBeDestroyed) selfdestruct(whale); 
            return;
        }else{ 
            if (msg.value < stake + DELTA) throw; 
            bool isOtherSuccess = msg.sender.send(stake); 
            setFacts(); 
            StakeIncreased("stake increased", whale, stake, blockheight);
        }
    }
    function destroyWhenRoundOver() onlyOwner{
        mustBeDestroyed = true;
    }
    function setNewPeriod(uint _newPeriod) onlyOwner{
        newPeriod = _newPeriod;
    }
    function getPeriod() constant returns (uint){
        return period;
    }
    function getNewPeriod() constant returns (uint){
        return newPeriod;
    }
    function getDestroyedWhenRoundOver() constant returns (bool){
        return mustBeDestroyed;
    }
    function getBlocksTillMatthew() public constant returns(uint){
        if (blockheight + period > block.number)
            return blockheight + period - block.number;
        else
            return 0;
    }
    modifier onlyOwner(){
        if (msg.sender != owner) throw;
        _;
    }
}

```

## RQ1_80d362cce2a6

SHA-256 `1df20ae9f1287734595fea4e1185795a5b71410cd5b52a8e5a3673fb6f33a957`

```solidity
pragma solidity ^0.4.15;
contract Owned {
    address public owner;
    function owned() {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address _newOwner) onlyOwner {
        owner = _newOwner;
    }
}
contract Mortal is Owned {
    function kill() onlyOwner {
        selfdestruct(owner);
    }
}
contract SafeMath {
    function safeAdd(uint256 x, uint256 y) internal returns(uint256) {
        uint256 z = x + y;
        assert((z >= x) && (z >= y));
        return z;
    }
    function safeSubtract(uint256 x, uint256 y) internal returns(uint256) {
        assert(x >= y);
        uint256 z = x - y;
        return z;
    }
    function safeMult(uint256 x, uint256 y) internal returns(uint256) {
        uint256 z = x * y;
        assert((x == 0)||(z/x == y));
        return z;
    }
}
contract Random is SafeMath {
    function getRand(uint blockNumber, uint max)
    public
    constant 
    returns(uint) {
        return(safeAdd(uint(sha3(block.blockhash(blockNumber))) % max, 1));
    }
}
contract LuckyNumber is Owned {
    uint256 public cost;
    uint8 public waitTime;
    uint256 public max;
    struct PendingNumber {
        address proxy;
        uint256 renderedNumber;
        uint256 creationBlockNumber;
        uint256 max;
        uint8 waitTime;
    }
    event EventLuckyNumberUpdated(uint256, uint256, uint8);
    event EventLuckyNumberRequested(address, uint256, uint256, uint8);
    event EventLuckyNumberRevealed(address, uint256, uint256);
    mapping (address => PendingNumber) public pendingNumbers;
    mapping (address => bool) public whiteList;
    function requestNumber(address _requestor, uint256 _max, uint8 _waitTime) payable public;
    function revealNumber(address _requestor) payable public;
}
contract LuckyNumberImp is LuckyNumber, Mortal, Random {
    function LuckyNumberImp() {
        owned();
        cost = 20000000000000000; 
        max = 15; 
        waitTime = 3; 
    }
    function setMax(uint256 _max)
    onlyOwner
    public
    returns (bool) {
        max = _max;
        EventLuckyNumberUpdated(cost, max, waitTime);
        return true;
    }
    function setWaitTime(uint8 _waitTime)
    onlyOwner
    public
    returns (bool) {
        waitTime = _waitTime;
        EventLuckyNumberUpdated(cost, max, waitTime);
        return true;
    }
    function setCost(uint256 _cost)
    onlyOwner
    public
    returns (bool) {
        cost = _cost;
        EventLuckyNumberUpdated(cost, max, waitTime);
        return true;
    }
    function enableProxy(address _proxy)
    onlyOwner
    public
    returns (bool) {
        whiteList[_proxy] = true;
        return whiteList[_proxy];
    }
    function removeProxy(address _proxy)
    onlyOwner
    public
    returns (bool) {
        delete whiteList[_proxy];
        return true;
    }
    function withdraw(address _recipient, uint256 _balance)
    onlyOwner
    public
    returns (bool) {
        _recipient.transfer(_balance);
        return true;
    }
    function () payable public {
        if (msg.sender != owner) {
            requestNumber(msg.sender, max, waitTime);
        }
    }
    function requestNumber(address _requestor, uint256 _max, uint8 _waitTime)
    payable 
    public {
        if (!whiteList[msg.sender]) {
            require(!(msg.value < cost));
        }
        assert(!checkNumber(_requestor));
        pendingNumbers[_requestor] = PendingNumber({
            proxy: tx.origin,
            renderedNumber: 0,
            max: max,
            creationBlockNumber: block.number,
            waitTime: waitTime
        });
        if (_max > 1) {
            pendingNumbers[_requestor].max = _max;
        }
        if (_waitTime > 0 && _waitTime < 250) {
            pendingNumbers[_requestor].waitTime = _waitTime;
        }
        EventLuckyNumberRequested(_requestor, pendingNumbers[_requestor].max, pendingNumbers[_requestor].creationBlockNumber, pendingNumbers[_requestor].waitTime);
    }
    function revealNumber(address _requestor)
    public
    payable {
        assert(_canReveal(_requestor, msg.sender));
        _revealNumber(_requestor);
    }
    function _revealNumber(address _requestor) 
    internal {
        uint256 luckyBlock = _revealBlock(_requestor);
        uint256 luckyNumber = getRand(luckyBlock, pendingNumbers[_requestor].max);
        pendingNumbers[_requestor].renderedNumber = luckyNumber;
        EventLuckyNumberRevealed(_requestor, pendingNumbers[_requestor].creationBlockNumber, pendingNumbers[_requestor].renderedNumber);
        pendingNumbers[_requestor].waitTime = 0;
    }
    function canReveal(address _requestor)
    public
    constant
    returns (bool, uint, uint, address, address) {
        return (_canReveal(_requestor, msg.sender), _remainingBlocks(_requestor), _revealBlock(_requestor), _requestor, msg.sender);
    }
    function _canReveal(address _requestor, address _proxy) 
    internal
    constant
    returns (bool) {
        if (checkNumber(_requestor)) {
            if (_remainingBlocks(_requestor) == 0) {
                if (pendingNumbers[_requestor].proxy == _requestor || pendingNumbers[_requestor].proxy == _proxy) {
                    return true;
                }
            }
        }
        return false;
    }
    function _remainingBlocks(address _requestor)
    internal
    constant
    returns (uint) {
        uint256 revealBlock = safeAdd(pendingNumbers[_requestor].creationBlockNumber, pendingNumbers[_requestor].waitTime);
        uint256 remainingBlocks = 0;
        if (revealBlock > block.number) {
            remainingBlocks = safeSubtract(revealBlock, block.number);
        }
        return remainingBlocks;
    }
    function _revealBlock(address _requestor)
    internal
    constant
    returns (uint) {
        return safeAdd(pendingNumbers[_requestor].creationBlockNumber, pendingNumbers[_requestor].waitTime);
    }
    function getNumber(address _requestor)
    public
    constant
    returns (uint, uint, uint, address) {
        return (pendingNumbers[_requestor].renderedNumber, pendingNumbers[_requestor].max, pendingNumbers[_requestor].creationBlockNumber, _requestor);
    }
    function checkNumber(address _requestor)
    public
    constant
    returns (bool) {
        if (pendingNumbers[_requestor].renderedNumber == 0 && pendingNumbers[_requestor].waitTime > 0) {
            return true;
        }
        return false;
    }
}
```

## RQ1_3843030989b1

SHA-256 `ae4d9472f18e80bcbb189d41cb19b9ca8716887330944b59598e8b9e962a1e64`

```solidity
pragma solidity ^0.4.19;
contract Lottery {
    address owner;
    address profit = 0xB7BB510B0746bdeE208dB6fB781bF5Be39d15A15;
    uint public tickets;
    uint public round;
    string public status;
    uint public lastWiningTicketNumber;
    address public lastWinner;
    address ticket1;
    address ticket2;
    address ticket3;
    address ticket4;
    address ticket5;
    uint constant price = 0.01 ether; 
    uint seed;
    bool entry = false;
    function Lottery() public { 
        owner = msg.sender;
        tickets = 5;
        round = 1;
        status = "Running";
        entry = false;
        seed = 777;
    }
    function changeStatus(string w) public {
        if (msg.sender == owner) {
            status = w;
        }
        else {
            revert();
        }
    }
    function changeSeed(uint32 n) public {
        if (msg.sender == owner) {
            seed = uint(n);
            seed = uint(block.blockhash(block.number-seed))%2000 + 1; 
        }
        else {
            revert();
        }
    }
    function () public payable { 
        buyTickets();
    }
    function buyTickets() public payable {
        if (entry == true) { 
            revert();
        }
        entry = true;
        if (msg.value != (price)) {
            entry = false;
            if (keccak256(status) == keccak256("Shutdown")) { 
                selfdestruct(owner);
            }
            revert(); 
        }
        else {
            if (tickets == 5) {
                tickets -= 1;
                ticket1 = msg.sender;
            }
            else if(tickets == 4) {
                tickets -= 1;
                ticket2 = msg.sender;
                profit.transfer(price * 1/2); 
            }
            else if(tickets == 3) {
                tickets -= 1;
                ticket3 = msg.sender;
            }
            else if(tickets == 2) {
                tickets -= 1;
                ticket4 = msg.sender;
            }
            else if(tickets == 1) {
                ticket5 = msg.sender;
                tickets = 5; 
                round += 1; 
                seed = uint(block.blockhash(block.number-seed))%2000 + 1; 
                uint random_number = uint(block.blockhash(block.number-seed))%5 + 1; 
                lastWiningTicketNumber = random_number; 
                uint pay = (price * 9/2); 
                if (random_number == 1) {
                    ticket1.transfer(pay);
                    lastWinner = ticket1; 
                }
                else if(random_number == 2) {
                    ticket2.transfer(pay);
                    lastWinner = ticket2; 
                }
                else if(random_number == 3) {
                    ticket3.transfer(pay);
                    lastWinner = ticket3; 
                }
                else if(random_number == 4) {
                    ticket4.transfer(pay);
                    lastWinner = ticket4; 
                }
                else if(random_number == 5) {
                    ticket5.transfer(pay);
                    lastWinner = ticket5; 
                }
            }
        }
        entry = false;
    }
}
```

## RQ1_451d90a0c512

SHA-256 `e354c01c5345452c437d357c38a9f3010716c6507e3edfa2e91f637ac11d9881`

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
contract KingOfNarnia {
  using SafeMath for uint256;  
  address public owner;
  address public king;
  string public kingsMessage;
  uint256 public bidExpireBlockLength = 12;
  uint256 public nextBidExpireBlockLength;
  uint256 public devFeePercent = 1;
  uint256 public rolloverPercent = 5;
  uint256 public lastBidAmount;
  uint256 public lastBidBlock;
  uint256 public currentRoundNumber;
  uint256 public currentBidNumber;
  uint256 public maxMessageChars = 140;
  mapping(uint256 => address) roundToKing;
  mapping(uint256 => uint256) roundToWinnings;
  mapping(uint256 => uint256) roundToFinalBid;
  mapping(uint256 => string) roundToFinalMessage;
  event NewKing(
    uint256 indexed roundNumber,
    address kingAddress,
    string kingMessage,
    uint256 bidAmount,
    uint256 indexed bidNumber,
    uint256 indexed bidBlockNumber
  );
  function KingOfTheEthill () public {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(owner == msg.sender);
    _;
  }
  function setDevFee (uint256 _n) onlyOwner() public {
	  require(_n >= 0 && _n <= 10);
    devFeePercent = _n;
  }
  function setRollover (uint256 _n) onlyOwner() public {
	  require(_n >= 1 && _n <= 30);
    rolloverPercent = _n;
  }
  function setNextBidExpireBlockLength (uint256 _n) onlyOwner() public {
	  require(_n >= 10 && _n <= 10000);
    nextBidExpireBlockLength = _n;
  }
  function setOwner (address _owner) onlyOwner() public {
    owner = _owner;
  }
  function bid (uint256 _roundNumber, string _message) payable public {
    require(!isContract(msg.sender));
    require(bytes(_message).length <= maxMessageChars);
    require(msg.value > 0);
    if (_roundNumber == currentRoundNumber && !roundExpired()) {
      require(msg.value > lastBidAmount);
    }else if (_roundNumber == (currentRoundNumber+1) && roundExpired()) {
      uint256 lastRoundPotBalance = address(this).balance.sub(msg.value);
      uint256 devFee = lastRoundPotBalance.mul(devFeePercent).div(100);
      owner.transfer(devFee);
      uint256 winnings = lastRoundPotBalance.sub(devFee).mul(100 - rolloverPercent).div(100);
      king.transfer(winnings);
      roundToKing[currentRoundNumber] = king;
      roundToWinnings[currentRoundNumber] = winnings;
      roundToFinalBid[currentRoundNumber] = lastBidAmount;
      roundToFinalMessage[currentRoundNumber] = kingsMessage;
      currentBidNumber = 0;
      currentRoundNumber++;
      if (nextBidExpireBlockLength != 0) {
        bidExpireBlockLength = nextBidExpireBlockLength;
        nextBidExpireBlockLength = 0;
      }
    }else {
      require(false);
    }
    king = msg.sender;
    kingsMessage = _message;
    lastBidAmount = msg.value;
    lastBidBlock = block.number;
    emit NewKing(currentRoundNumber, king, kingsMessage, lastBidAmount, currentBidNumber, lastBidBlock);
    currentBidNumber++;
  }
  function roundExpired() public view returns (bool) {
    return blocksSinceLastBid() >= bidExpireBlockLength;
  }
  function blocksRemaining() public view returns (uint256) {
    if (roundExpired()) {
      return 0;
    }else {
      return bidExpireBlockLength - blocksSinceLastBid();
    }
  }
  function blocksSinceLastBid() public view returns (uint256) {
    return block.number - lastBidBlock;
  }
  function estimateNextPotSeedAmount() public view returns (uint256) {
      return address(this).balance.mul(100 - devFeePercent).div(100).mul(rolloverPercent).div(100);
  }
  function getRoundState() public view returns (bool _currentRoundExpired, uint256 _nextRoundPotSeedAmountEstimate, uint256 _roundNumber, uint256 _bidNumber, address _king, string _kingsMessage, uint256 _lastBidAmount, uint256 _blocksRemaining, uint256 _potAmount, uint256 _blockNumber, uint256 _bidExpireBlockLength) {
    _currentRoundExpired = roundExpired();
    _nextRoundPotSeedAmountEstimate = estimateNextPotSeedAmount();
    _roundNumber = currentRoundNumber;
    _bidNumber = currentBidNumber;
    _king = king;
    _kingsMessage = kingsMessage;
    _lastBidAmount = lastBidAmount;
    _blocksRemaining = blocksRemaining();
    _potAmount = address(this).balance;
    _blockNumber = block.number;
    _bidExpireBlockLength = bidExpireBlockLength;
  }
  function getPastRound(uint256 _roundNum) public view returns (address _kingAddress, uint256 _finalBid, uint256 _kingWinnings, string _finalMessage) {
    _kingAddress = roundToKing[_roundNum]; 
    _kingWinnings = roundToWinnings[_roundNum];
    _finalBid = roundToFinalBid[_roundNum];
    _finalMessage = roundToFinalMessage[_roundNum];
  }
  function isContract(address addr) internal view returns (bool) {
    uint size;
    assembly { size := extcodesize(addr) }
    return size > 0;
  }
}

```

## RQ1_faed8e9e25ab

SHA-256 `809787f7fdea2c9d25fdd3359548be0f6f7be6b1117296afa615bcaa0b8b78e2`

```solidity
pragma solidity ^0.4.24;
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract multiowned {
    struct PendingState {
        uint yetNeeded;
        uint ownersDone;
        uint index;
    }
    event Confirmation(address owner, bytes32 operation);
    event Revoke(address owner, bytes32 operation);
    event OwnerChanged(address oldOwner, address newOwner);
    event OwnerAdded(address newOwner);
    event OwnerRemoved(address oldOwner);
    event RequirementChanged(uint newRequirement);
    modifier onlyowner {
        if (isOwner(msg.sender))
            _;
    }
    modifier onlymanyowners(bytes32 _operation) {
        if (confirmAndCheck(_operation))
            _;
    }
    constructor(address[] _owners, uint _required) public {
        m_numOwners = _owners.length;
        for (uint i = 0; i < _owners.length; ++i)
        {
            m_owners[1 + i] = uint(_owners[i]);
            m_ownerIndex[uint(_owners[i])] = 1 + i;
        }
        m_required = _required;
    }
    function revoke(bytes32 _operation) external {
        uint ownerIndex = m_ownerIndex[uint(msg.sender)];
        if (ownerIndex == 0) return;
        uint ownerIndexBit = 2**ownerIndex;
        PendingState storage pending = m_pending[_operation];
        if (pending.ownersDone & ownerIndexBit > 0) {
            pending.yetNeeded++;
            pending.ownersDone -= ownerIndexBit;
            emit Revoke(msg.sender, _operation);
        }
    }
    function changeOwner(address _from, address _to) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        if (isOwner(_to)) return;
        uint ownerIndex = m_ownerIndex[uint(_from)];
        if (ownerIndex == 0) return;
        clearPending();
        m_owners[ownerIndex] = uint(_to);
        m_ownerIndex[uint(_from)] = 0;
        m_ownerIndex[uint(_to)] = ownerIndex;
        emit OwnerChanged(_from, _to);
    }
    function addOwner(address _owner) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        if (isOwner(_owner)) return;
        clearPending();
        if (m_numOwners >= c_maxOwners)
            reorganizeOwners();
        if (m_numOwners >= c_maxOwners)
            return;
        m_numOwners++;
        m_owners[m_numOwners] = uint(_owner);
        m_ownerIndex[uint(_owner)] = m_numOwners;
        emit OwnerAdded(_owner);
    }
    function removeOwner(address _owner) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        uint ownerIndex = m_ownerIndex[uint(_owner)];
        if (ownerIndex == 0) return;
        if (m_required > m_numOwners - 1) return;
        m_owners[ownerIndex] = 0;
        m_ownerIndex[uint(_owner)] = 0;
        clearPending();
        reorganizeOwners(); 
        emit OwnerRemoved(_owner);
    }
    function changeRequirement(uint _newRequired) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        if (_newRequired > m_numOwners) return;
        m_required = _newRequired;
        clearPending();
        emit RequirementChanged(_newRequired);
    }
    function isOwner(address _addr) public view returns (bool) {
        return m_ownerIndex[uint(_addr)] > 0;
    }
    function hasConfirmed(bytes32 _operation, address _owner) public view returns (bool) {
        PendingState storage pending = m_pending[_operation];
        uint ownerIndex = m_ownerIndex[uint(_owner)];
        if (ownerIndex == 0) return false;
        uint ownerIndexBit = 2**ownerIndex;
        if (pending.ownersDone & ownerIndexBit == 0) {
            return false;
        } else {
            return true;
        }
    }
    function confirmAndCheck(bytes32 _operation) internal returns (bool) {
        uint ownerIndex = m_ownerIndex[uint(msg.sender)];
        if (ownerIndex == 0) return;
        PendingState storage pending = m_pending[_operation];
        if (pending.yetNeeded == 0) {
            pending.yetNeeded = m_required;
            pending.ownersDone = 0;
            pending.index = m_pendingIndex.length++;
            m_pendingIndex[pending.index] = _operation;
        }
        uint ownerIndexBit = 2**ownerIndex;
        if (pending.ownersDone & ownerIndexBit == 0) {
            emit Confirmation(msg.sender, _operation);
            if (pending.yetNeeded <= 1) {
                delete m_pendingIndex[m_pending[_operation].index];
                delete m_pending[_operation];
                return true;
            }
            else
            {
                pending.yetNeeded--;
                pending.ownersDone |= ownerIndexBit;
            }
        }
    }
    function reorganizeOwners() private returns (bool) {
        uint free = 1;
        while (free < m_numOwners)
        {
            while (free < m_numOwners && m_owners[free] != 0) free++;
            while (m_numOwners > 1 && m_owners[m_numOwners] == 0) m_numOwners--;
            if (free < m_numOwners && m_owners[m_numOwners] != 0 && m_owners[free] == 0)
            {
                m_owners[free] = m_owners[m_numOwners];
                m_ownerIndex[m_owners[free]] = free;
                m_owners[m_numOwners] = 0;
            }
        }
    }
    function clearPending() internal {
        uint length = m_pendingIndex.length;
        for (uint i = 0; i < length; ++i) {
            if (m_pendingIndex[i] != 0) {
                delete m_pending[m_pendingIndex[i]];
            }
        }
        delete m_pendingIndex;
    }
    uint public m_required;
    uint public m_numOwners;
    uint[256] m_owners;
    uint constant c_maxOwners = 250;
    mapping(uint => uint) m_ownerIndex;
    mapping(bytes32 => PendingState) m_pending;
    bytes32[] m_pendingIndex;
}
contract daylimit is multiowned {
    modifier limitedDaily(uint _value) {
        if (underLimit(_value))
            _;
    }
    constructor(uint _limit) public {
        m_dailyLimit = _limit;
        m_lastDay = today();
    }
    function setDailyLimit(uint _newLimit) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        m_dailyLimit = _newLimit;
    }
    function resetSpentToday() onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        m_spentToday = 0;
    }
    function underLimit(uint _value) internal onlyowner returns (bool) {
        if (today() > m_lastDay) {
            m_spentToday = 0;
            m_lastDay = today();
        }
        if (m_spentToday + _value >= m_spentToday && m_spentToday + _value <= m_dailyLimit) {
            m_spentToday += _value;
            return true;
        }
        return false;
    }
    function today() private view returns (uint) { return block.timestamp / 1 days; }
    uint public m_dailyLimit;
    uint public m_spentToday;
    uint public m_lastDay;
}
contract multisig {
    event Deposit(address from, uint value);
    event SingleTransact(address owner, uint value, address to);
    event MultiTransact(address owner, bytes32 operation, uint value, address to);
    event ConfirmationERC20Needed(bytes32 operation, address initiator, uint value, address to, ERC20Basic token);
    event ConfirmationETHNeeded(bytes32 operation, address initiator, uint value, address to);
    function changeOwner(address _from, address _to) external;
}
contract Wallet is multisig, multiowned, daylimit {
    uint public version = 4;
    struct Transaction {
        address to;
        uint value;
        address token;
    }
    ERC20Basic public erc20;
    constructor(address[] _owners, uint _required, uint _daylimit, address _erc20)
            multiowned(_owners, _required) daylimit(_daylimit) public {
            erc20 = ERC20Basic(_erc20);
    }
    function changeERC20(address _erc20) onlymanyowners(keccak256(abi.encodePacked(msg.data))) public {
        erc20 = ERC20Basic(_erc20);
    }
    function kill(address _to) onlymanyowners(keccak256(abi.encodePacked(msg.data))) external {
        selfdestruct(_to);
    }
    function() public payable {
        if (msg.value > 0)
            emit Deposit(msg.sender, msg.value);
    }
    function transferETH(address _to, uint _value) external onlyowner returns (bytes32 _r) {
        if (underLimit(_value)) {
            emit SingleTransact(msg.sender, _value, _to);
            _to.transfer(_value);
            return 0;
        }
        _r = keccak256(abi.encodePacked(msg.data, block.number));
        if (!confirmETH(_r) && m_txs[_r].to == 0) {
            m_txs[_r].to = _to;
            m_txs[_r].value = _value;
            emit ConfirmationETHNeeded(_r, msg.sender, _value, _to);
        }
    }
    function confirmETH(bytes32 _h) onlymanyowners(_h) public returns (bool) {
        if (m_txs[_h].to != 0) {
            m_txs[_h].to.transfer(m_txs[_h].value);
            emit MultiTransact(msg.sender, _h, m_txs[_h].value, m_txs[_h].to);
            delete m_txs[_h];
            return true;
        }
    }
    function transferERC20(address _to, uint _value) external onlyowner returns (bytes32 _r) {
        if (underLimit(_value)) {
            emit SingleTransact(msg.sender, _value, _to);
            erc20.transfer(_to, _value);
            return 0;
        }
        _r = keccak256(abi.encodePacked(msg.data, block.number));
        if (!confirmERC20(_r) && m_txs[_r].to == 0) {
            m_txs[_r].to = _to;
            m_txs[_r].value = _value;
            m_txs[_r].token = erc20;
            emit ConfirmationERC20Needed(_r, msg.sender, _value, _to, erc20);
        }
    }
    function confirmERC20(bytes32 _h) onlymanyowners(_h) public returns (bool) {
        if (m_txs[_h].to != 0) {
            ERC20Basic token = ERC20Basic(m_txs[_h].token);
            token.transfer(m_txs[_h].to, m_txs[_h].value);
            emit MultiTransact(msg.sender, _h, m_txs[_h].value, m_txs[_h].to);
            delete m_txs[_h];
            return true;
        }
    }
    function clearPending() internal {
        uint length = m_pendingIndex.length;
        for (uint i = 0; i < length; ++i)
            delete m_txs[m_pendingIndex[i]];
        super.clearPending();
    }
    mapping (bytes32 => Transaction) m_txs;
}
```

## RQ1_9978e161eb68

SHA-256 `5b778c8ae05e3a478391bb968647a9548c70c499da52953265cab3b87d489d76`

```solidity
pragma solidity ^0.4.22;
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
contract CryptoCurrencyNetworkToken {
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
interface Token { 
    function distr(address _to, uint256 _value) external returns (bool);
    function totalSupply() constant external returns (uint256 supply);
    function balanceOf(address _owner) constant external returns (uint256 balance);
}
contract CryptoCurrencyNetwork is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "CryptoCurrencyNetwork";
    string public constant symbol = "CCN";
    uint public constant decimals = 18;
uint256 public totalSupply = 100000000e18;
uint256 public totalDistributed = 15000000e18;
uint256 public totalRemaining = totalSupply.sub(totalDistributed);
uint256 public value = 500e18;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
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
    modifier onlyWhitelist() {
        require(blacklist[msg.sender] == false);
        _;
    }
    function CCN() public {
        owner = msg.sender;
        balances[owner] = totalDistributed;
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
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr onlyWhitelist public {
        if (value > totalRemaining) {
            value = totalRemaining;
        }
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        value = value.div(100000).mul(99999);
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
        CryptoCurrencyNetworkToken t = CryptoCurrencyNetworkToken(tokenAddress);
        uint bal = t.balanceOf(who);
        return bal;
    }
    function withdraw() onlyOwner public {
        uint256 etherBalance = address(this).balance;
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
    function withdrawCryptoCurrencyNetworkTokens(address _tokenContract) onlyOwner public returns (bool) {
        CryptoCurrencyNetworkToken token = CryptoCurrencyNetworkToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_f82d8856631a

SHA-256 `8522b64bdc6b1deb234c7543cb6df424909c7da4ea7940d5d7a826cadacd9ce8`

```solidity
pragma solidity ^0.4.18;
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
contract HOTTO is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "HOTTO";
    string public constant symbol = "HT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 10000000000e8; 
    uint256 public totalDistributed = 3000000000e8;    
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
    function HT () public {
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
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
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
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
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
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
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
        Burn(burner, _value);
    }
    function withdrawForeignTokens(address _tokenContract) onlyOwner public returns (bool) {
        ForeignToken token = ForeignToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_6bc986b54c91

SHA-256 `7b6281c038d313139a5f628f86d5143245c068088676367af64a81824dc13cff`

```solidity
pragma solidity 0.4.24;
contract SelfAuthorized {
    modifier authorized() {
        require(msg.sender == address(this), "Method can only be called from this contract");
        _;
    }
}
contract ErrorUtils {
    event LogError(string methodSig, string errMsg);
    event LogErrorWithHintBytes32(bytes32 indexed bytes32Value, string methodSig, string errMsg);
    event LogErrorWithHintAddress(address indexed addressValue, string methodSig, string errMsg);
}
contract WETH9 {
    string public name     = "Wrapped Ether";
    string public symbol   = "WETH";
    uint8  public decimals = 18;
    event  Approval(address indexed _owner, address indexed _spender, uint _value);
    event  Transfer(address indexed _from, address indexed _to, uint _value);
    event  Deposit(address indexed _owner, uint _value);
    event  Withdrawal(address indexed _owner, uint _value);
    mapping (address => uint)                       public  balanceOf;
    mapping (address => mapping (address => uint))  public  allowance;
    function() public payable {
        deposit();
    }
    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
        Deposit(msg.sender, msg.value);
    }
    function withdraw(uint wad) public {
        require(balanceOf[msg.sender] >= wad);
        balanceOf[msg.sender] -= wad;
        msg.sender.transfer(wad);
        Withdrawal(msg.sender, wad);
    }
    function totalSupply() public view returns (uint) {
        return this.balance;
    }
    function approve(address guy, uint wad) public returns (bool) {
        allowance[msg.sender][guy] = wad;
        Approval(msg.sender, guy, wad);
        return true;
    }
    function transfer(address dst, uint wad) public returns (bool) {
        return transferFrom(msg.sender, dst, wad);
    }
    function transferFrom(address src, address dst, uint wad)
        public
        returns (bool)
    {
        require(balanceOf[src] >= wad);
        if (src != msg.sender && allowance[src][msg.sender] != uint(-1)) {
            require(allowance[src][msg.sender] >= wad);
            allowance[src][msg.sender] -= wad;
        }
        balanceOf[src] -= wad;
        balanceOf[dst] += wad;
        Transfer(src, dst, wad);
        return true;
    }
}
contract Utils {
    modifier addressValid(address _address) {
        require(_address != address(0), "Utils::_ INVALID_ADDRESS");
        _;
    }
}
contract DSAuthority {
    function canCall(address src, address dst, bytes4 sig) public view returns (bool);
}
contract DSAuthEvents {
    event LogSetAuthority (address indexed authority);
    event LogSetOwner     (address indexed owner);
}
contract DSAuth is DSAuthEvents {
    DSAuthority  public  authority;
    address      public  owner;
    constructor() public {
        owner = msg.sender;
        emit LogSetOwner(msg.sender);
    }
    function setOwner(address owner_)
        public
        auth
    {
        owner = owner_;
        emit LogSetOwner(owner);
    }
    function setAuthority(DSAuthority authority_)
        public
        auth
    {
        authority = authority_;
        emit LogSetAuthority(authority);
    }
    modifier auth {
        require(isAuthorized(msg.sender, msg.sig), "DSAuth::_ SENDER_NOT_AUTHORIZED");
        _;
    }
    function isAuthorized(address src, bytes4 sig) internal view returns (bool) {
        if (src == address(this)) {
            return true;
        } else if (src == owner) {
            return true;
        } else if (authority == DSAuthority(0)) {
            return false;
        } else {
            return authority.canCall(src, this, sig);
        }
    }
}
contract DSNote {
    event LogNote(
        bytes4   indexed  sig,
        address  indexed  guy,
        bytes32  indexed  foo,
        bytes32  indexed  bar,
        uint              wad,
        bytes             fax
    ) anonymous;
    modifier note {
        bytes32 foo;
        bytes32 bar;
        assembly {
            foo := calldataload(4)
            bar := calldataload(36)
        }
        emit LogNote(msg.sig, msg.sender, foo, bar, msg.value, msg.data);
        _;
    }
}
interface ERC20 {
    function name() external view returns(string);
    function symbol() external view returns(string);
    function decimals() external view returns(uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address tokenOwner) external view returns (uint balance);
    function allowance(address tokenOwner, address spender) external view returns (uint remaining);
    function transfer(address to, uint tokens) external returns (bool success);
    function approve(address spender, uint tokens) external returns (bool success);
    function transferFrom(address from, address to, uint tokens) external returns (bool success);
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract MasterCopy is SelfAuthorized {
    address masterCopy;
    function changeMasterCopy(address _masterCopy)
        public
        authorized
    {
        require(_masterCopy != 0, "Invalid master copy address provided");
        masterCopy = _masterCopy;
    }
}
contract Config is DSNote, DSAuth, Utils {
    WETH9 public weth9;
    mapping (address => bool) public isAccountHandler;
    mapping (address => bool) public isAdmin;
    address[] public admins;
    bool public disableAdminControl = false;
    event LogAdminAdded(address indexed _admin, address _by);
    event LogAdminRemoved(address indexed _admin, address _by);
    constructor() public {
        admins.push(msg.sender);
        isAdmin[msg.sender] = true;
    }
    modifier onlyAdmin(){
        require(isAdmin[msg.sender], "Config::_ SENDER_NOT_AUTHORIZED");
        _;
    }
    function setWETH9
    (
        address _weth9
    ) 
        public
        auth
        note
        addressValid(_weth9) 
    {
        weth9 = WETH9(_weth9);
    }
    function setAccountHandler
    (
        address _accountHandler,
        bool _isAccountHandler
    )
        public
        auth
        note
        addressValid(_accountHandler)
    {
        isAccountHandler[_accountHandler] = _isAccountHandler;
    }
    function toggleAdminsControl() 
        public
        auth
        note
    {
        disableAdminControl = !disableAdminControl;
    }
    function isAdminValid(address _admin)
        public
        view
        returns (bool)
    {
        if(disableAdminControl) {
            return true;
        } else {
            return isAdmin[_admin];
        }
    }
    function getAllAdmins()
        public
        view
        returns(address[])
    {
        return admins;
    }
    function addAdmin
    (
        address _admin
    )
        external
        note
        onlyAdmin
        addressValid(_admin)
    {   
        require(!isAdmin[_admin], "Config::addAdmin ADMIN_ALREADY_EXISTS");
        admins.push(_admin);
        isAdmin[_admin] = true;
        emit LogAdminAdded(_admin, msg.sender);
    }
    function removeAdmin
    (
        address _admin
    ) 
        external
        note
        onlyAdmin
        addressValid(_admin)
    {   
        require(isAdmin[_admin], "Config::removeAdmin ADMIN_DOES_NOT_EXIST");
        require(msg.sender != _admin, "Config::removeAdmin ADMIN_NOT_AUTHORIZED");
        isAdmin[_admin] = false;
        for (uint i = 0; i < admins.length - 1; i++) {
            if (admins[i] == _admin) {
                admins[i] = admins[admins.length - 1];
                admins.length -= 1;
                break;
            }
        }
        emit LogAdminRemoved(_admin, msg.sender);
    }
}
library ECRecovery {
    function recover(bytes32 _hash, bytes _sig)
        internal
        pure
    returns (address)
    {
        bytes32 r;
        bytes32 s;
        uint8 v;
        if (_sig.length != 65) {
            return (address(0));
        }
        assembly {
            r := mload(add(_sig, 32))
            s := mload(add(_sig, 64))
            v := byte(0, mload(add(_sig, 96)))
        }
        if (v < 27) {
            v += 27;
        }
        if (v != 27 && v != 28) {
            return (address(0));
        } else {
            return ecrecover(_hash, v, r, s);
        }
    }
    function toEthSignedMessageHash(bytes32 _hash)
        internal
        pure
    returns (bytes32)
    {
        return keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", _hash)
        );
    }
}
contract Utils2 {
    using ECRecovery for bytes32;
    function _recoverSigner(bytes32 _hash, bytes _signature) 
        internal
        pure
        returns(address _signer)
    {
        return _hash.toEthSignedMessageHash().recover(_signature);
    }
}
contract Account is MasterCopy, DSNote, Utils, Utils2, ErrorUtils {
    address[] public users;
    mapping (address => bool) public isUser;
    mapping (bytes32 => bool) public actionCompleted;
    WETH9 public weth9;
    Config public config;
    bool public isInitialized = false;
    event LogTransferBySystem(address indexed token, address indexed to, uint value, address by);
    event LogTransferByUser(address indexed token, address indexed to, uint value, address by);
    event LogUserAdded(address indexed user, address by);
    event LogUserRemoved(address indexed user, address by);
    event LogImplChanged(address indexed newImpl, address indexed oldImpl);
    modifier initialized() {
        require(isInitialized, "Account::_ ACCOUNT_NOT_INITIALIZED");
        _;
    }
    modifier notInitialized() {
        require(!isInitialized, "Account::_ ACCOUNT_ALREADY_INITIALIZED");
        _;
    }
    modifier userExists(address _user) {
        require(isUser[_user], "Account::_ INVALID_USER");
        _;
    }
    modifier userDoesNotExist(address _user) {
        require(!isUser[_user], "Account::_ USER_DOES_NOT_EXISTS");
        _;
    }
    modifier onlyAdmin() {
        require(config.isAdminValid(msg.sender), "Account::_ INVALID_ADMIN_ACCOUNT");
        _;
    }
    modifier onlyHandler(){
        require(config.isAccountHandler(msg.sender), "Account::_ INVALID_ACC_HANDLER");
        _;
    }
    function init(address _user, address _config)
        public 
        notInitialized
    {
        users.push(_user);
        isUser[_user] = true;
        config = Config(_config);
        weth9 = config.weth9();
        isInitialized = true;
    }
    function getAllUsers() public view returns (address[]) {
        return users;
    }
    function balanceFor(address _token) public view returns (uint _balance){
        _balance = ERC20(_token).balanceOf(this);
    }
    function transferBySystem
    (   
        address _token,
        address _to,
        uint _value
    ) 
        external 
        onlyHandler
        note 
        initialized
    {
        require(ERC20(_token).balanceOf(this) >= _value, "Account::transferBySystem INSUFFICIENT_BALANCE_IN_ACCOUNT");
        ERC20(_token).transfer(_to, _value);
        emit LogTransferBySystem(_token, _to, _value, msg.sender);
    }
    function transferByUser
    (   
        address _token,
        address _to,
        uint _value,
        uint _salt,
        bytes _signature
    )
        external
        addressValid(_to)
        note
        initialized
        onlyAdmin
    {
        bytes32 actionHash = _getTransferActionHash(_token, _to, _value, _salt);
        if(actionCompleted[actionHash]) {
            emit LogError("Account::transferByUser", "ACTION_ALREADY_PERFORMED");
            return;
        }
        if(ERC20(_token).balanceOf(this) < _value){
            emit LogError("Account::transferByUser", "INSUFFICIENT_BALANCE_IN_ACCOUNT");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(!isUser[signer]) {
            emit LogError("Account::transferByUser", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        if (_token == address(weth9)) {
            weth9.withdraw(_value);
            _to.transfer(_value);
        } else {
            require(ERC20(_token).transfer(_to, _value), "Account::transferByUser TOKEN_TRANSFER_FAILED");
        }
        emit LogTransferByUser(_token, _to, _value, signer);
    }
    function addUser
    (
        address _user,
        uint _salt,
        bytes _signature
    )
        external 
        note 
        addressValid(_user)
        userDoesNotExist(_user)
        initialized
        onlyAdmin
    {   
        bytes32 actionHash = _getUserActionHash(_user, "ADD_USER", _salt);
        if(actionCompleted[actionHash])
        {
            emit LogError("Account::addUser", "ACTION_ALREADY_PERFORMED");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(!isUser[signer]) {
            emit LogError("Account::addUser", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        users.push(_user);
        isUser[_user] = true;
        emit LogUserAdded(_user, signer);
    }
    function removeUser
    (
        address _user,
        uint _salt,
        bytes _signature
    ) 
        external
        note
        userExists(_user) 
        initialized
        onlyAdmin
    {   
        bytes32 actionHash = _getUserActionHash(_user, "REMOVE_USER", _salt);
        if(actionCompleted[actionHash]) {
            emit LogError("Account::removeUser", "ACTION_ALREADY_PERFORMED");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(users.length == 1){
            emit LogError("Account::removeUser",  "ACC_SHOULD_HAVE_ATLEAST_ONE_USER");
            return;
        }
        if(!isUser[signer]){
            emit LogError("Account::removeUser", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        isUser[_user] = false;
        for (uint i = 0; i < users.length - 1; i++) {
            if (users[i] == _user) {
                users[i] = users[users.length - 1];
                users.length -= 1;
                break;
            }
        }
        emit LogUserRemoved(_user, signer);
    }
    function _getTransferActionHash
    ( 
        address _token,
        address _to,
        uint _value,
        uint _salt
    ) 
        internal
        view
        returns (bytes32)
    {
        return keccak256(
            abi.encodePacked(
                address(this),
                _token,
                _to,
                _value,
                _salt
            )
        );
    }
    function _getUserActionHash
    ( 
        address _user,
        string _action,
        uint _salt
    ) 
        internal
        view
        returns (bytes32)
    {
        return keccak256(
            abi.encodePacked(
                address(this),
                _user,
                _action,
                _salt
            )
        );
    }
    function() external payable {
        require(msg.data.length == 0 && msg.value > 0, "Account::fallback INVALID_ETHER_TRANSFER");
        if(msg.sender != address(weth9)){
            weth9.deposit.value(msg.value)();
        }
    }
    function changeImpl
    (
        address _to,
        uint _salt,
        bytes _signature
    )
        external 
        note 
        addressValid(_to)
        initialized
        onlyAdmin
    {   
        bytes32 actionHash = _getUserActionHash(_to, "CHANGE_ACCOUNT_IMPLEMENTATION", _salt);
        if(actionCompleted[actionHash])
        {
            emit LogError("Account::changeImpl", "ACTION_ALREADY_PERFORMED");
            return;
        }
        address signer = _recoverSigner(actionHash, _signature);
        if(!isUser[signer]) {
            emit LogError("Account::changeImpl", "SIGNER_NOT_AUTHORIZED_WITH_ACCOUNT");
            return;
        }
        actionCompleted[actionHash] = true;
        address oldImpl = masterCopy;
        this.changeMasterCopy(_to);
        emit LogImplChanged(_to, oldImpl);
    }
}
```

## RQ1_ab71daf07a5e

SHA-256 `b45a3ac724056940017a8031569d22fefcd193d5a0f095fe5cfc68bcc1c818b7`

```solidity
contract GameOfThrones {
    address public trueGods;
    address public jester;
    uint public lastCollection;
    uint public onThrone;
    uint public kingCost;
    uint public piggyBank;
    uint public godBank;
    uint public jesterBank;
    uint public kingBank;
    address[] public citizensAddresses;
    uint[] public citizensAmounts;
    uint32 public totalCitizens;
    uint32 public lastCitizenPaid;
    address public madKing;
    uint32 public round;
    uint public amountAlreadyPaidBack;
    uint public amountInvested;
    uint constant TWENTY_FOUR_HOURS = 60 * 60 * 24;
    uint constant PEACE_PERIOD = 60 * 60 * 240;
    function GameOfThrones() {
        trueGods = msg.sender;
        madKing = msg.sender;
        jester = msg.sender;
        lastCollection = block.timestamp;
        onThrone = block.timestamp;
        kingCost = 1 ether;
        amountAlreadyPaidBack = 0;
        amountInvested = 0;
        totalCitizens = 0;
    }
    function repairTheCastle() returns(bool) {
        uint amount = msg.value;
        if (amount < 10 finney) {
            msg.sender.send(msg.value);
            return false;
        }
        if (amount > 100 ether) {
            msg.sender.send(msg.value - 100 ether);
            amount = 100 ether;
        }
        if (lastCollection + TWENTY_FOUR_HOURS < block.timestamp) {
            if (totalCitizens == 1) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 95 / 100);
            } else if (totalCitizens == 2) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 60 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 35 / 100);
            } else if (totalCitizens >= 3) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 50 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 30 / 100);
                citizensAddresses[citizensAddresses.length - 3].send(piggyBank * 15 / 100);
            }
            godBank += piggyBank * 5 / 100;
            piggyBank = 0;
            jester = msg.sender;
            citizensAddresses.push(msg.sender);
            citizensAmounts.push(amount * 110 / 100);
            totalCitizens += 1;
            investInTheSystem(amount);
            godAutomaticCollectFee();
            piggyBank += amount;
            round += 1;
        } else {
            citizensAddresses.push(msg.sender);
            citizensAmounts.push(amount * 110 / 100);
            totalCitizens += 1;
            investInTheSystem(amount);
            piggyBank += (amount * 5 / 100);
            while (citizensAmounts[lastCitizenPaid] < (address(this).balance - piggyBank - godBank - kingBank - jesterBank) && lastCitizenPaid <= totalCitizens) {
                citizensAddresses[lastCitizenPaid].send(citizensAmounts[lastCitizenPaid]);
                amountAlreadyPaidBack += citizensAmounts[lastCitizenPaid];
                lastCitizenPaid += 1;
            }
        }
    }
    function() {
        repairTheCastle();
    }
    function investInTheSystem(uint amount) internal {
        lastCollection = block.timestamp;
        amountInvested += amount;
        jesterBank += amount * 5 / 100;
        kingBank += amount * 5 / 100;
        piggyBank += (amount * 5 / 100);
        kingAutomaticCollectFee();
        jesterAutomaticCollectFee();
    }
    function newKing(address newKing) {
        if (msg.sender == madKing) {
            madKing = newKing;
            kingCost = 1 ether;
        }
    }
    function bribery() {
        uint amount = 100 finney;
        if (msg.value >= amount) {
            jester.send(jesterBank);
            jesterBank = 0;
            jester = msg.sender;
            msg.sender.send(msg.value - amount);
            investInTheSystem(amount);
        } else {
            throw;
        }
    }
    function usurpation() {
        if (msg.sender == madKing) {
            investInTheSystem(msg.value);
            kingCost += msg.value;
        } else {
            if (onThrone + PEACE_PERIOD <= block.timestamp && msg.value >= kingCost * 110 / 100) {
                madKing.send(kingBank);
                godBank += msg.value * 5 / 100;
                investInTheSystem(msg.value);
                kingCost = msg.value;
                madKing = msg.sender;
                onThrone = block.timestamp;
            } else {
                throw;
            }
        }
    }
    function collectFee() {
        if (msg.sender == trueGods) {
            trueGods.send(godBank);
        }
    }
    function godAutomaticCollectFee() internal {
        if (godBank >= 1 ether) {
          trueGods.send(godBank);
          godBank = 0;
        }
    }
    function kingAutomaticCollectFee() internal {
        if (kingBank >= 100 finney) {
          madKing.send(kingBank);
          kingBank = 0;
        }
    }
    function jesterAutomaticCollectFee() internal {
        if (jesterBank >= 100 finney) {
          jester.send(jesterBank);
          jesterBank = 0;
        }
    }
}
```

## RQ1_e7801f3e61cb

SHA-256 `cdf1bfc603f350d951e7ff9604f3f0cae50f0a99c0bca9e6948a396fe327cfe0`

```solidity
pragma solidity ^0.4.24;
contract ILiquidPledgingPlugin {
    function beforeTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount ) returns (uint maxAllowed);
    function afterTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount
    );
}
pragma solidity ^0.4.15;
contract Owned {
    address public owner;
    address public newOwnerCandidate;
    event OwnershipRequested(address indexed by, address indexed to);
    event OwnershipTransferred(address indexed from, address indexed to);
    event OwnershipRemoved();
    function Owned() public {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        require (msg.sender == owner);
        _;
    }
    function proposeOwnership(address _newOwnerCandidate) public onlyOwner {
        newOwnerCandidate = _newOwnerCandidate;
        OwnershipRequested(msg.sender, newOwnerCandidate);
    }
    function acceptOwnership() public {
        require(msg.sender == newOwnerCandidate);
        address oldOwner = owner;
        owner = newOwnerCandidate;
        newOwnerCandidate = 0x0;
        OwnershipTransferred(oldOwner, owner);
    }
    function changeOwnership(address _newOwner) public onlyOwner {
        require(_newOwner != 0x0);
        address oldOwner = owner;
        owner = _newOwner;
        newOwnerCandidate = 0x0;
        OwnershipTransferred(oldOwner, owner);
    }
    function removeOwnership(address _dac) public onlyOwner {
        require(_dac == 0xdac);
        owner = 0x0;
        newOwnerCandidate = 0x0;
        OwnershipRemoved();     
    }
} 
pragma solidity ^0.4.15;
contract ERC20 {
    function totalSupply() public constant returns (uint256 supply);
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
pragma solidity ^0.4.15;
contract Escapable is Owned {
    address public escapeHatchCaller;
    address public escapeHatchDestination;
    mapping (address=>bool) private escapeBlacklist; 
    function Escapable(address _escapeHatchCaller, address _escapeHatchDestination) public {
        escapeHatchCaller = _escapeHatchCaller;
        escapeHatchDestination = _escapeHatchDestination;
    }
    modifier onlyEscapeHatchCallerOrOwner {
        require ((msg.sender == escapeHatchCaller)||(msg.sender == owner));
        _;
    }
    function blacklistEscapeToken(address _token) internal {
        escapeBlacklist[_token] = true;
        EscapeHatchBlackistedToken(_token);
    }
    function isTokenEscapable(address _token) constant public returns (bool) {
        return !escapeBlacklist[_token];
    }
    function escapeHatch(address _token) public onlyEscapeHatchCallerOrOwner {   
        require(escapeBlacklist[_token]==false);
        uint256 balance;
        if (_token == 0x0) {
            balance = this.balance;
            escapeHatchDestination.transfer(balance);
            EscapeHatchCalled(_token, balance);
            return;
        }
        ERC20 token = ERC20(_token);
        balance = token.balanceOf(this);
        require(token.transfer(escapeHatchDestination, balance));
        EscapeHatchCalled(_token, balance);
    }
    function changeHatchEscapeCaller(address _newEscapeHatchCaller) public onlyEscapeHatchCallerOrOwner {
        escapeHatchCaller = _newEscapeHatchCaller;
    }
    event EscapeHatchBlackistedToken(address token);
    event EscapeHatchCalled(address token, uint amount);
}
pragma solidity ^0.4.11;
interface LPVault {
    function authorizePayment(bytes32 _ref, address _dest, uint _amount);
    function () payable;
}
contract LiquidPledgingBase is Escapable {
    uint constant MAX_DELEGATES = 10;
    uint constant MAX_SUBPROJECT_LEVEL = 20;
    uint constant MAX_INTERPROJECT_LEVEL = 20;
    enum PledgeAdminType { Giver, Delegate, Project }
    enum PledgeState { Pledged, Paying, Paid }
    struct PledgeAdmin { 
        PledgeAdminType adminType; 
        address addr; 
        string name;
        string url;  
        uint64 commitTime;  
        uint64 parentProject;  
        bool canceled;      
        ILiquidPledgingPlugin plugin; 
    }
    struct Pledge {
        uint amount;
        uint64 owner; 
        uint64[] delegationChain; 
        uint64 intendedProject; 
        uint64 commitTime;  
        uint64 oldPledge; 
        PledgeState pledgeState; 
    }
    Pledge[] pledges;
    PledgeAdmin[] admins; 
    LPVault public vault;
    mapping (bytes32 => uint64) hPledge2idx;
    mapping (bytes32 => bool) pluginWhitelist;
    bool public usePluginWhitelist = true;
    modifier onlyVault() {
        require(msg.sender == address(vault));
        _;
    }
    function LiquidPledgingBase(
        address _vault,
        address _escapeHatchCaller,
        address _escapeHatchDestination
    ) Escapable(_escapeHatchCaller, _escapeHatchDestination) public {
        admins.length = 1; 
        pledges.length = 1; 
        vault = LPVault(_vault); 
    }
    function addGiver(
        string name,
        string url,
        uint64 commitTime,
        ILiquidPledgingPlugin plugin
    ) returns (uint64 idGiver) {
        require(isValidPlugin(plugin)); 
        idGiver = uint64(admins.length);
        admins.push(PledgeAdmin(
            PledgeAdminType.Giver,
            msg.sender,
            name,
            url,
            commitTime,
            0,
            false,
            plugin));
        GiverAdded(idGiver);
    }
    event GiverAdded(uint64 indexed idGiver);
    function updateGiver(
        uint64 idGiver,
        address newAddr,
        string newName,
        string newUrl,
        uint64 newCommitTime)
    {
        PledgeAdmin storage giver = findAdmin(idGiver);
        require(giver.adminType == PledgeAdminType.Giver); 
        require(giver.addr == msg.sender); 
        giver.addr = newAddr;
        giver.name = newName;
        giver.url = newUrl;
        giver.commitTime = newCommitTime;
        GiverUpdated(idGiver);
    }
    event GiverUpdated(uint64 indexed idGiver);
    function addDelegate(
        string name,
        string url,
        uint64 commitTime,
        ILiquidPledgingPlugin plugin
    ) returns (uint64 idDelegate) { 
        require(isValidPlugin(plugin)); 
        idDelegate = uint64(admins.length);
        admins.push(PledgeAdmin(
            PledgeAdminType.Delegate,
            msg.sender,
            name,
            url,
            commitTime,
            0,
            false,
            plugin));
        DelegateAdded(idDelegate);
    }
    event DelegateAdded(uint64 indexed idDelegate);
    function updateDelegate(
        uint64 idDelegate,
        address newAddr,
        string newName,
        string newUrl,
        uint64 newCommitTime) {
        PledgeAdmin storage delegate = findAdmin(idDelegate);
        require(delegate.adminType == PledgeAdminType.Delegate);
        require(delegate.addr == msg.sender);
        delegate.addr = newAddr;
        delegate.name = newName;
        delegate.url = newUrl;
        delegate.commitTime = newCommitTime;
        DelegateUpdated(idDelegate);
    }
    event DelegateUpdated(uint64 indexed idDelegate);
    function addProject(
        string name,
        string url,
        address projectAdmin,
        uint64 parentProject,
        uint64 commitTime,
        ILiquidPledgingPlugin plugin
    ) returns (uint64 idProject) {
        require(isValidPlugin(plugin));
        if (parentProject != 0) {
            PledgeAdmin storage pa = findAdmin(parentProject);
            require(pa.adminType == PledgeAdminType.Project);
            require(getProjectLevel(pa) < MAX_SUBPROJECT_LEVEL);
        }
        idProject = uint64(admins.length);
        admins.push(PledgeAdmin(
            PledgeAdminType.Project,
            projectAdmin,
            name,
            url,
            commitTime,
            parentProject,
            false,
            plugin));
        ProjectAdded(idProject);
    }
    event ProjectAdded(uint64 indexed idProject);
    function updateProject(
        uint64 idProject,
        address newAddr,
        string newName,
        string newUrl,
        uint64 newCommitTime)
    {
        PledgeAdmin storage project = findAdmin(idProject);
        require(project.adminType == PledgeAdminType.Project);
        require(project.addr == msg.sender);
        project.addr = newAddr;
        project.name = newName;
        project.url = newUrl;
        project.commitTime = newCommitTime;
        ProjectUpdated(idProject);
    }
    event ProjectUpdated(uint64 indexed idAdmin);
    function numberOfPledges() constant returns (uint) {
        return pledges.length - 1;
    }
    function getPledge(uint64 idPledge) constant returns(
        uint amount,
        uint64 owner,
        uint64 nDelegates,
        uint64 intendedProject,
        uint64 commitTime,
        uint64 oldPledge,
        PledgeState pledgeState
    ) {
        Pledge storage p = findPledge(idPledge);
        amount = p.amount;
        owner = p.owner;
        nDelegates = uint64(p.delegationChain.length);
        intendedProject = p.intendedProject;
        commitTime = p.commitTime;
        oldPledge = p.oldPledge;
        pledgeState = p.pledgeState;
    }
    function getPledgeDelegate(uint64 idPledge, uint idxDelegate) constant returns(
        uint64 idDelegate,
        address addr,
        string name
    ) {
        Pledge storage p = findPledge(idPledge);
        idDelegate = p.delegationChain[idxDelegate - 1];
        PledgeAdmin storage delegate = findAdmin(idDelegate);
        addr = delegate.addr;
        name = delegate.name;
    }
    function numberOfPledgeAdmins() constant returns(uint) {
        return admins.length - 1;
    }
    function getPledgeAdmin(uint64 idAdmin) constant returns (
        PledgeAdminType adminType,
        address addr,
        string name,
        string url,
        uint64 commitTime,
        uint64 parentProject,
        bool canceled,
        address plugin)
    {
        PledgeAdmin storage m = findAdmin(idAdmin);
        adminType = m.adminType;
        addr = m.addr;
        name = m.name;
        url = m.url;
        commitTime = m.commitTime;
        parentProject = m.parentProject;
        canceled = m.canceled;
        plugin = address(m.plugin);
    }
    function findOrCreatePledge(
        uint64 owner,
        uint64[] delegationChain,
        uint64 intendedProject,
        uint64 commitTime,
        uint64 oldPledge,
        PledgeState state
        ) internal returns (uint64)
    {
        bytes32 hPledge = sha3(
            owner, delegationChain, intendedProject, commitTime, oldPledge, state);
        uint64 idx = hPledge2idx[hPledge];
        if (idx > 0) return idx;
        idx = uint64(pledges.length);
        hPledge2idx[hPledge] = idx;
        pledges.push(Pledge(
            0, owner, delegationChain, intendedProject, commitTime, oldPledge, state));
        return idx;
    }
    function findAdmin(uint64 idAdmin) internal returns (PledgeAdmin storage) {
        require(idAdmin < admins.length);
        return admins[idAdmin];
    }
    function findPledge(uint64 idPledge) internal returns (Pledge storage) {
        require(idPledge < pledges.length);
        return pledges[idPledge];
    }
    uint64 constant  NOTFOUND = 0xFFFFFFFFFFFFFFFF;
    function getDelegateIdx(Pledge p, uint64 idDelegate) internal returns(uint64) {
        for (uint i=0; i < p.delegationChain.length; i++) {
            if (p.delegationChain[i] == idDelegate) return uint64(i);
        }
        return NOTFOUND;
    }
    function getPledgeLevel(Pledge p) internal returns(uint) {
        if (p.oldPledge == 0) return 0;
        Pledge storage oldN = findPledge(p.oldPledge);
        return getPledgeLevel(oldN) + 1; 
    }
    function maxCommitTime(Pledge p) internal returns(uint commitTime) {
        PledgeAdmin storage m = findAdmin(p.owner);
        commitTime = m.commitTime; 
        for (uint i=0; i<p.delegationChain.length; i++) {
            m = findAdmin(p.delegationChain[i]);
            if (m.commitTime > commitTime) commitTime = m.commitTime;
        }
    }
    function getProjectLevel(PledgeAdmin m) internal returns(uint) {
        assert(m.adminType == PledgeAdminType.Project);
        if (m.parentProject == 0) return(1);
        PledgeAdmin storage parentNM = findAdmin(m.parentProject);
        return getProjectLevel(parentNM) + 1;
    }
    function isProjectCanceled(uint64 projectId) constant returns (bool) {
        PledgeAdmin storage m = findAdmin(projectId);
        if (m.adminType == PledgeAdminType.Giver) return false;
        assert(m.adminType == PledgeAdminType.Project);
        if (m.canceled) return true;
        if (m.parentProject == 0) return false;
        return isProjectCanceled(m.parentProject);
    }
    function getOldestPledgeNotCanceled(uint64 idPledge
        ) internal constant returns(uint64) {
        if (idPledge == 0) return 0;
        Pledge storage p = findPledge(idPledge);
        PledgeAdmin storage admin = findAdmin(p.owner);
        if (admin.adminType == PledgeAdminType.Giver) return idPledge;
        assert(admin.adminType == PledgeAdminType.Project);
        if (!isProjectCanceled(p.owner)) return idPledge;
        return getOldestPledgeNotCanceled(p.oldPledge);
    }
    function checkAdminOwner(PledgeAdmin m) internal constant {
        require((msg.sender == m.addr) || (msg.sender == address(m.plugin)));
    }
    function addValidPlugin(bytes32 contractHash) external onlyOwner {
        pluginWhitelist[contractHash] = true;
    }
    function removeValidPlugin(bytes32 contractHash) external onlyOwner {
        pluginWhitelist[contractHash] = false;
    }
    function useWhitelist(bool useWhitelist) external onlyOwner {
        usePluginWhitelist = useWhitelist;
    }
    function isValidPlugin(address addr) public returns(bool) {
        if (!usePluginWhitelist || addr == 0x0) return true;
        bytes32 contractHash = getCodeHash(addr);
        return pluginWhitelist[contractHash];
    }
    function getCodeHash(address addr) public returns(bytes32) {
        bytes memory o_code;
        assembly {
            let size := extcodesize(addr)
            o_code := mload(0x40)
            mstore(0x40, add(o_code, and(add(add(size, 0x20), 0x1f), not(0x1f))))
            mstore(o_code, size)
            extcodecopy(addr, add(o_code, 0x20), 0, size)
        }
        return keccak256(o_code);
    }
}
pragma solidity ^0.4.11;
contract LiquidPledging is LiquidPledgingBase {
    function LiquidPledging(
        address _vault,
        address _escapeHatchCaller,
        address _escapeHatchDestination
    ) LiquidPledgingBase(_vault, _escapeHatchCaller, _escapeHatchDestination) {
    }
    function donate(uint64 idGiver, uint64 idReceiver) payable {
        if (idGiver == 0) {
            idGiver = addGiver("", "", 259200, ILiquidPledgingPlugin(0x0));
        }
        PledgeAdmin storage sender = findAdmin(idGiver);
        checkAdminOwner(sender);
        require(sender.adminType == PledgeAdminType.Giver);
        uint amount = msg.value;
        require(amount > 0);
        vault.transfer(amount); 
        uint64 idPledge = findOrCreatePledge(
            idGiver,
            new uint64[](0), 
            0,
            0,
            0,
            PledgeState.Pledged
        );
        Pledge storage nTo = findPledge(idPledge);
        nTo.amount += amount;
        Transfer(0, idPledge, amount); 
        transfer(idGiver, idPledge, amount, idReceiver); 
    }
    function transfer( 
        uint64 idSender,
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ){
        idPledge = normalizePledge(idPledge);
        Pledge storage p = findPledge(idPledge);
        PledgeAdmin storage receiver = findAdmin(idReceiver);
        PledgeAdmin storage sender = findAdmin(idSender);
        checkAdminOwner(sender);
        require(p.pledgeState == PledgeState.Pledged);
        if (p.owner == idSender) {
            if (receiver.adminType == PledgeAdminType.Giver) {
                transferOwnershipToGiver(idPledge, amount, idReceiver);
            } else if (receiver.adminType == PledgeAdminType.Project) {
                transferOwnershipToProject(idPledge, amount, idReceiver);
            } else if (receiver.adminType == PledgeAdminType.Delegate) {
                uint recieverDIdx = getDelegateIdx(p, idReceiver);
                if (p.intendedProject > 0 && recieverDIdx != NOTFOUND) {
                    if (recieverDIdx == p.delegationChain.length - 1) {
                        uint64 toPledge = findOrCreatePledge(
                            p.owner,
                            p.delegationChain,
                            0,
                            0,
                            p.oldPledge,
                            PledgeState.Pledged);
                        doTransfer(idPledge, toPledge, amount);
                    } else {
                        undelegate(idPledge, amount, p.delegationChain.length - receiverDIdx - 1);
                    }
                } else {
                    idPledge = undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length
                    );
                    appendDelegate(idPledge, amount, idReceiver);
                }
            } else {
                assert(false);
            }
            return;
        }
        uint senderDIdx = getDelegateIdx(p, idSender);
        if (senderDIdx != NOTFOUND) {
            if (receiver.adminType == PledgeAdminType.Giver) {
                assert(p.owner == idReceiver);
                undelegate(idPledge, amount, p.delegationChain.length);
                return;
            }
            if (receiver.adminType == PledgeAdminType.Delegate) {
                uint receiverDIdx = getDelegateIdx(p, idReceiver);
                if (receiverDIdx == NOTFOUND) {
                    idPledge = undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length - senderDIdx - 1
                    );
                    appendDelegate(idPledge, amount, idReceiver);
                } else if (receiverDIdx > senderDIdx) {
                    idPledge = undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length - senderDIdx - 1
                    );
                    appendDelegate(idPledge, amount, idReceiver);
                } else if (receiverDIdx <= senderDIdx) {
                    undelegate(
                        idPledge,
                        amount,
                        p.delegationChain.length - receiverDIdx - 1
                    );
                }
                return;
            }
            if (receiver.adminType == PledgeAdminType.Project) {
                idPledge = undelegate(
                    idPledge,
                    amount,
                    p.delegationChain.length - senderDIdx - 1
                );
                proposeAssignProject(idPledge, amount, idReceiver);
                return;
            }
        }
        assert(false);  
    }
    function withdraw(uint64 idPledge, uint amount) {
        idPledge = normalizePledge(idPledge); 
        Pledge storage p = findPledge(idPledge);
        require(p.pledgeState == PledgeState.Pledged);
        PledgeAdmin storage owner = findAdmin(p.owner);
        checkAdminOwner(owner);
        uint64 idNewPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Paying
        );
        doTransfer(idPledge, idNewPledge, amount);
        vault.authorizePayment(bytes32(idNewPledge), owner.addr, amount);
    }
    function confirmPayment(uint64 idPledge, uint amount) onlyVault {
        Pledge storage p = findPledge(idPledge);
        require(p.pledgeState == PledgeState.Paying);
        uint64 idNewPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Paid
        );
        doTransfer(idPledge, idNewPledge, amount);
    }
    function cancelPayment(uint64 idPledge, uint amount) onlyVault {
        Pledge storage p = findPledge(idPledge);
        require(p.pledgeState == PledgeState.Paying); 
        uint64 oldPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        oldPledge = normalizePledge(oldPledge);
        doTransfer(idPledge, oldPledge, amount);
    }
    function cancelProject(uint64 idProject) { 
        PledgeAdmin storage project = findAdmin(idProject);
        checkAdminOwner(project);
        project.canceled = true;
        CancelProject(idProject);
    }
    function cancelPledge(uint64 idPledge, uint amount) { 
        idPledge = normalizePledge(idPledge);
        Pledge storage p = findPledge(idPledge);
        require(p.oldPledge != 0);
        PledgeAdmin storage m = findAdmin(p.owner);
        checkAdminOwner(m);
        uint64 oldPledge = getOldestPledgeNotCanceled(p.oldPledge);
        doTransfer(idPledge, oldPledge, amount);
    }
    uint constant D64 = 0x10000000000000000;
    function mTransfer(
        uint64 idSender,
        uint[] pledgesAmounts,
        uint64 idReceiver
    ) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            transfer(idSender, idPledge, amount, idReceiver);
        }
    }
    function mWithdraw(uint[] pledgesAmounts) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            withdraw(idPledge, amount);
        }
    }
    function mConfirmPayment(uint[] pledgesAmounts) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            confirmPayment(idPledge, amount);
        }
    }
    function mCancelPayment(uint[] pledgesAmounts) {
        for (uint i = 0; i < pledgesAmounts.length; i++ ) {
            uint64 idPledge = uint64( pledgesAmounts[i] & (D64-1) );
            uint amount = pledgesAmounts[i] / D64;
            cancelPayment(idPledge, amount);
        }
    }
    function mNormalizePledge(uint64[] pledges) {
        for (uint i = 0; i < pledges.length; i++ ) {
            normalizePledge( pledges[i] );
        }
    }
    function transferOwnershipToProject(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        Pledge storage p = findPledge(idPledge);
        require(getPledgeLevel(p) < MAX_INTERPROJECT_LEVEL);
        require(!isProjectCanceled(idReceiver));
        uint64 oldPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        uint64 toPledge = findOrCreatePledge(
            idReceiver,                     
            new uint64[](0),                
            0,
            0,
            oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }   
    function transferOwnershipToGiver(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        uint64 toPledge = findOrCreatePledge(
            idReceiver,
            new uint64[](0),
            0,
            0,
            0,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }
    function appendDelegate(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        Pledge storage p = findPledge(idPledge);
        require(p.delegationChain.length < MAX_DELEGATES);
        uint64[] memory newDelegationChain = new uint64[](
            p.delegationChain.length + 1
        );
        for (uint i = 0; i<p.delegationChain.length; i++) {
            newDelegationChain[i] = p.delegationChain[i];
        }
        newDelegationChain[p.delegationChain.length] = idReceiver;
        uint64 toPledge = findOrCreatePledge(
            p.owner,
            newDelegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }
    function undelegate(
        uint64 idPledge,
        uint amount,
        uint q
    ) internal returns (uint64)
    {
        Pledge storage p = findPledge(idPledge);
        uint64[] memory newDelegationChain = new uint64[](
            p.delegationChain.length - q
        );
        for (uint i=0; i<p.delegationChain.length - q; i++) {
            newDelegationChain[i] = p.delegationChain[i];
        }
        uint64 toPledge = findOrCreatePledge(
            p.owner,
            newDelegationChain,
            0,
            0,
            p.oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
        return toPledge;
    }
    function proposeAssignProject(
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) internal {
        Pledge storage p = findPledge(idPledge);
        require(getPledgeLevel(p) < MAX_INTERPROJECT_LEVEL);
        require(!isProjectCanceled(idReceiver));
        uint64 toPledge = findOrCreatePledge(
            p.owner,
            p.delegationChain,
            idReceiver,
            uint64(getTime() + maxCommitTime(p)),
            p.oldPledge,
            PledgeState.Pledged
        );
        doTransfer(idPledge, toPledge, amount);
    }
    function doTransfer(uint64 from, uint64 to, uint _amount) internal {
        uint amount = callPlugins(true, from, to, _amount);
        if (from == to) { 
            return;
        }
        if (amount == 0) {
            return;
        }
        Pledge storage nFrom = findPledge(from);
        Pledge storage nTo = findPledge(to);
        require(nFrom.amount >= amount);
        nFrom.amount -= amount;
        nTo.amount += amount;
        Transfer(from, to, amount);
        callPlugins(false, from, to, amount);
    }
    function normalizePledge(uint64 idPledge) returns(uint64) {
        Pledge storage p = findPledge(idPledge);
        if (p.pledgeState != PledgeState.Pledged) {
            return idPledge;
        }
        if ((p.intendedProject > 0) && ( getTime() > p.commitTime)) {
            uint64 oldPledge = findOrCreatePledge(
                p.owner,
                p.delegationChain,
                0,
                0,
                p.oldPledge,
                PledgeState.Pledged
            );
            uint64 toPledge = findOrCreatePledge(
                p.intendedProject,
                new uint64[](0),
                0,
                0,
                oldPledge,
                PledgeState.Pledged
            );
            doTransfer(idPledge, toPledge, p.amount);
            idPledge = toPledge;
            p = findPledge(idPledge);
        }
        toPledge = getOldestPledgeNotCanceled(idPledge);
        if (toPledge != idPledge) {
            doTransfer(idPledge, toPledge, p.amount);
        }
        return toPledge;
    }
    function callPlugin(
        bool before,
        uint64 adminId,
        uint64 fromPledge,
        uint64 toPledge,
        uint64 context,
        uint amount
    ) internal returns (uint allowedAmount) {
        uint newAmount;
        allowedAmount = amount;
        PledgeAdmin storage admin = findAdmin(adminId);
        if ((address(admin.plugin) != 0) && (allowedAmount > 0)) {
            if (before) {
                newAmount = admin.plugin.beforeTransfer(
                    adminId,
                    fromPledge,
                    toPledge,
                    context,
                    amount
                );
                require(newAmount <= allowedAmount);
                allowedAmount = newAmount;
            } else {
                admin.plugin.afterTransfer(
                    adminId,
                    fromPledge,
                    toPledge,
                    context,
                    amount
                );
            }
        }
    }
    function callPluginsPledge(
        bool before,
        uint64 idPledge,
        uint64 fromPledge,
        uint64 toPledge,
        uint amount
    ) internal returns (uint allowedAmount) {
        uint64 offset = idPledge == fromPledge ? 0 : 256;
        allowedAmount = amount;
        Pledge storage p = findPledge(idPledge);
        allowedAmount = callPlugin(
            before,
            p.owner,
            fromPledge,
            toPledge,
            offset,
            allowedAmount
        );
        for (uint64 i=0; i<p.delegationChain.length; i++) {
            allowedAmount = callPlugin(
                before,
                p.delegationChain[i],
                fromPledge,
                toPledge,
                offset + i+1,
                allowedAmount
            );
        }
        if (p.intendedProject > 0) {
            allowedAmount = callPlugin(
                before,
                p.intendedProject,
                fromPledge,
                toPledge,
                offset + 255,
                allowedAmount
            );
        }
    }
    function callPlugins(
        bool before,
        uint64 fromPledge,
        uint64 toPledge,
        uint amount
    ) internal returns (uint allowedAmount) {
        allowedAmount = amount;
        allowedAmount = callPluginsPledge(
            before,
            fromPledge,
            fromPledge,
            toPledge,
            allowedAmount
        );
        allowedAmount = callPluginsPledge(
            before,
            toPledge,
            fromPledge,
            toPledge,
            allowedAmount
        );
    }
    function getTime() internal returns (uint) {
        return now;
    }
    event Transfer(uint64 indexed from, uint64 indexed to, uint amount);
    event CancelProject(uint64 indexed idProject);
}
pragma solidity ^0.4.18;
contract Controlled {
    modifier onlyController { require(msg.sender == controller); _; }
    address public controller;
    function Controlled() public { controller = msg.sender;}
    function changeController(address _newController) public onlyController {
        controller = _newController;
    }
}
pragma solidity ^0.4.18;
contract TokenController {
    function proxyPayment(address _owner) public payable returns(bool);
    function onTransfer(address _from, address _to, uint _amount) public returns(bool);
    function onApprove(address _owner, address _spender, uint _amount) public
        returns(bool);
}
pragma solidity ^0.4.18;
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 _amount, address _token, bytes _data) public;
}
contract MiniMeToken is Controlled {
    string public name;                
    uint8 public decimals;             
    string public symbol;              
    string public version = 'MMT_0.2'; 
    struct  Checkpoint {
        uint128 fromBlock;
        uint128 value;
    }
    MiniMeToken public parentToken;
    uint public parentSnapShotBlock;
    uint public creationBlock;
    mapping (address => Checkpoint[]) balances;
    mapping (address => mapping (address => uint256)) allowed;
    Checkpoint[] totalSupplyHistory;
    bool public transfersEnabled;
    MiniMeTokenFactory public tokenFactory;
    function MiniMeToken(
        address _tokenFactory,
        address _parentToken,
        uint _parentSnapShotBlock,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        bool _transfersEnabled
    ) public {
        tokenFactory = MiniMeTokenFactory(_tokenFactory);
        name = _tokenName;                                 
        decimals = _decimalUnits;                          
        symbol = _tokenSymbol;                             
        parentToken = MiniMeToken(_parentToken);
        parentSnapShotBlock = _parentSnapShotBlock;
        transfersEnabled = _transfersEnabled;
        creationBlock = block.number;
    }
    function transfer(address _to, uint256 _amount) public returns (bool success) {
        require(transfersEnabled);
        return doTransfer(msg.sender, _to, _amount);
    }
    function transferFrom(address _from, address _to, uint256 _amount
    ) public returns (bool success) {
        if (msg.sender != controller) {
            require(transfersEnabled);
            if (allowed[_from][msg.sender] < _amount) return false;
            allowed[_from][msg.sender] -= _amount;
        }
        return doTransfer(_from, _to, _amount);
    }
    function doTransfer(address _from, address _to, uint _amount
    ) internal returns(bool) {
           if (_amount == 0) {
               return true;
           }
           require(parentSnapShotBlock < block.number);
           require((_to != 0) && (_to != address(this)));
           var previousBalanceFrom = balanceOfAt(_from, block.number);
           if (previousBalanceFrom < _amount) {
               return false;
           }
           if (isContract(controller)) {
               require(TokenController(controller).onTransfer(_from, _to, _amount));
           }
           updateValueAtNow(balances[_from], previousBalanceFrom - _amount);
           var previousBalanceTo = balanceOfAt(_to, block.number);
           require(previousBalanceTo + _amount >= previousBalanceTo); 
           updateValueAtNow(balances[_to], previousBalanceTo + _amount);
           Transfer(_from, _to, _amount);
           return true;
    }
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balanceOfAt(_owner, block.number);
    }
    function approve(address _spender, uint256 _amount) public returns (bool success) {
        require(transfersEnabled);
        require((_amount == 0) || (allowed[msg.sender][_spender] == 0));
        if (isContract(controller)) {
            require(TokenController(controller).onApprove(msg.sender, _spender, _amount));
        }
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }
    function allowance(address _owner, address _spender
    ) public constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function approveAndCall(address _spender, uint256 _amount, bytes _extraData
    ) public returns (bool success) {
        require(approve(_spender, _amount));
        ApproveAndCallFallBack(_spender).receiveApproval(
            msg.sender,
            _amount,
            this,
            _extraData
        );
        return true;
    }
    function totalSupply() public constant returns (uint) {
        return totalSupplyAt(block.number);
    }
    function balanceOfAt(address _owner, uint _blockNumber) public constant
        returns (uint) {
        if ((balances[_owner].length == 0)
            || (balances[_owner][0].fromBlock > _blockNumber)) {
            if (address(parentToken) != 0) {
                return parentToken.balanceOfAt(_owner, min(_blockNumber, parentSnapShotBlock));
            } else {
                return 0;
            }
        } else {
            return getValueAt(balances[_owner], _blockNumber);
        }
    }
    function totalSupplyAt(uint _blockNumber) public constant returns(uint) {
        if ((totalSupplyHistory.length == 0)
            || (totalSupplyHistory[0].fromBlock > _blockNumber)) {
            if (address(parentToken) != 0) {
                return parentToken.totalSupplyAt(min(_blockNumber, parentSnapShotBlock));
            } else {
                return 0;
            }
        } else {
            return getValueAt(totalSupplyHistory, _blockNumber);
        }
    }
    function createCloneToken(
        string _cloneTokenName,
        uint8 _cloneDecimalUnits,
        string _cloneTokenSymbol,
        uint _snapshotBlock,
        bool _transfersEnabled
        ) public returns(address) {
        if (_snapshotBlock == 0) _snapshotBlock = block.number;
        MiniMeToken cloneToken = tokenFactory.createCloneToken(
            this,
            _snapshotBlock,
            _cloneTokenName,
            _cloneDecimalUnits,
            _cloneTokenSymbol,
            _transfersEnabled
            );
        cloneToken.changeController(msg.sender);
        NewCloneToken(address(cloneToken), _snapshotBlock);
        return address(cloneToken);
    }
    function generateTokens(address _owner, uint _amount
    ) public onlyController returns (bool) {
        uint curTotalSupply = totalSupply();
        require(curTotalSupply + _amount >= curTotalSupply); 
        uint previousBalanceTo = balanceOf(_owner);
        require(previousBalanceTo + _amount >= previousBalanceTo); 
        updateValueAtNow(totalSupplyHistory, curTotalSupply + _amount);
        updateValueAtNow(balances[_owner], previousBalanceTo + _amount);
        Transfer(0, _owner, _amount);
        return true;
    }
    function destroyTokens(address _owner, uint _amount
    ) onlyController public returns (bool) {
        uint curTotalSupply = totalSupply();
        require(curTotalSupply >= _amount);
        uint previousBalanceFrom = balanceOf(_owner);
        require(previousBalanceFrom >= _amount);
        updateValueAtNow(totalSupplyHistory, curTotalSupply - _amount);
        updateValueAtNow(balances[_owner], previousBalanceFrom - _amount);
        Transfer(_owner, 0, _amount);
        return true;
    }
    function enableTransfers(bool _transfersEnabled) public onlyController {
        transfersEnabled = _transfersEnabled;
    }
    function getValueAt(Checkpoint[] storage checkpoints, uint _block
    ) constant internal returns (uint) {
        if (checkpoints.length == 0) return 0;
        if (_block >= checkpoints[checkpoints.length-1].fromBlock)
            return checkpoints[checkpoints.length-1].value;
        if (_block < checkpoints[0].fromBlock) return 0;
        uint min = 0;
        uint max = checkpoints.length-1;
        while (max > min) {
            uint mid = (max + min + 1)/ 2;
            if (checkpoints[mid].fromBlock<=_block) {
                min = mid;
            } else {
                max = mid-1;
            }
        }
        return checkpoints[min].value;
    }
    function updateValueAtNow(Checkpoint[] storage checkpoints, uint _value
    ) internal  {
        if ((checkpoints.length == 0)
        || (checkpoints[checkpoints.length -1].fromBlock < block.number)) {
               Checkpoint storage newCheckPoint = checkpoints[ checkpoints.length++ ];
               newCheckPoint.fromBlock =  uint128(block.number);
               newCheckPoint.value = uint128(_value);
           } else {
               Checkpoint storage oldCheckPoint = checkpoints[checkpoints.length-1];
               oldCheckPoint.value = uint128(_value);
           }
    }
    function isContract(address _addr) constant internal returns(bool) {
        uint size;
        if (_addr == 0) return false;
        assembly {
            size := extcodesize(_addr)
        }
        return size>0;
    }
    function min(uint a, uint b) pure internal returns (uint) {
        return a < b ? a : b;
    }
    function () public payable {
        require(isContract(controller));
        require(TokenController(controller).proxyPayment.value(msg.value)(msg.sender));
    }
    function claimTokens(address _token) public onlyController {
        if (_token == 0x0) {
            controller.transfer(this.balance);
            return;
        }
        MiniMeToken token = MiniMeToken(_token);
        uint balance = token.balanceOf(this);
        token.transfer(controller, balance);
        ClaimedTokens(_token, controller, balance);
    }
    event ClaimedTokens(address indexed _token, address indexed _controller, uint _amount);
    event Transfer(address indexed _from, address indexed _to, uint256 _amount);
    event NewCloneToken(address indexed _cloneToken, uint _snapshotBlock);
    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _amount
        );
}
contract MiniMeTokenFactory {
    function createCloneToken(
        address _parentToken,
        uint _snapshotBlock,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        bool _transfersEnabled
    ) public returns (MiniMeToken) {
        MiniMeToken newToken = new MiniMeToken(
            this,
            _parentToken,
            _snapshotBlock,
            _tokenName,
            _decimalUnits,
            _tokenSymbol,
            _transfersEnabled
            );
        newToken.changeController(msg.sender);
        return newToken;
    }
}
pragma solidity ^0.4.17;
contract LPPDacs is Escapable, TokenController {
    uint constant FROM_FIRST_DELEGATE = 1;
    uint constant TO_FIRST_DELEGATE = 257;
    LiquidPledging public liquidPledging;
    struct Dac {
        MiniMeToken token;
        address owner;
    }
    mapping (uint64 => Dac) dacs;
    event GenerateTokens(uint64 indexed idDelegate, address addr, uint amount);
    event DestroyTokens(uint64 indexed idDelegate, address addr, uint amount);
    function LPPDacs(
        LiquidPledging _liquidPledging,
        address _escapeHatchCaller,
        address _escapeHatchDestination
    ) Escapable(_escapeHatchCaller, _escapeHatchDestination) public
    {
        liquidPledging = _liquidPledging;
    }
    function beforeTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount
    ) external returns (uint maxAllowed)
    {
        require(msg.sender == address(liquidPledging));
        return amount;
    }
    function afterTransfer(
        uint64 pledgeManager,
        uint64 pledgeFrom,
        uint64 pledgeTo,
        uint64 context,
        uint amount
    ) external
    {
        require(msg.sender == address(liquidPledging));
        var (, toOwner, , toIntendedProject, , , toPledgeState ) = liquidPledging.getPledge(pledgeTo);
        var (, fromOwner, , , , , ) = liquidPledging.getPledge(pledgeFrom);
        var (toAdminType, toAddr, , , , , , ) = liquidPledging.getPledgeAdmin(toOwner);
        Dac storage d;
        uint64 idDelegate;
        if (context == FROM_FIRST_DELEGATE &&
                toIntendedProject == 0 &&
                toAdminType == LiquidPledgingBase.PledgeAdminType.Project &&
                toOwner != fromOwner &&
                toPledgeState == LiquidPledgingBase.PledgeState.Pledged)
        {
            (idDelegate, , ) = liquidPledging.getPledgeDelegate(pledgeFrom, 1);
            d = dacs[idDelegate];
            require(address(d.token) != 0x0);
            var (, fromAddr , , , , , , ) = liquidPledging.getPledgeAdmin(fromOwner);
            d.token.generateTokens(fromAddr, amount);
            GenerateTokens(idDelegate, fromAddr, amount);
        }
        if ( (context == TO_FIRST_DELEGATE) &&
            liquidPledging.isProjectCanceled(fromOwner)) {
            (idDelegate, , ) = liquidPledging.getPledgeDelegate(pledgeTo, 1);
            d = dacs[idDelegate];
            require(address(d.token) != 0x0);
            if (d.token.balanceOf(toAddr) >= amount) {
                d.token.destroyTokens(toAddr, amount);
                DestroyTokens(fromOwner, toAddr, amount);
            }
        }
    }
    function addDac(
        string name,
        string url,
        uint64 commitTime,
        string tokenName,
        string tokenSymbol
    ) public
    {
        uint64 idDelegate = liquidPledging.addDelegate(
            name,
            url,
            commitTime,
            ILiquidPledgingPlugin(this)
        );
        MiniMeTokenFactory tokenFactory = new MiniMeTokenFactory();
        MiniMeToken token = new MiniMeToken(tokenFactory, 0x0, 0, tokenName, 18, tokenSymbol, false);
        dacs[idDelegate] = Dac(token, msg.sender);
    }
    function addDac(
        string name,
        string url,
        uint64 commitTime,
        MiniMeToken token
    ) public
    {
        uint64 idDelegate = liquidPledging.addDelegate(
          name,
          url,
          commitTime,
          ILiquidPledgingPlugin(this)
        );
        dacs[idDelegate] = Dac(token, msg.sender);
    }
    function transfer(
        uint64 idDelegate,
        uint64 idPledge,
        uint amount,
        uint64 idReceiver
    ) public
    {
        Dac storage d = dacs[idDelegate];
        require(msg.sender == d.owner);
        liquidPledging.transfer(
            idDelegate,
            idPledge,
            amount,
            idReceiver
        );
    }
    function changeOwner(
        uint64 idDelegate,
        address newOwner
    ) public
    {
        Dac storage d = dacs[idDelegate];
        require(msg.sender == d.owner);
        d.owner = newOwner;
    }
    function updateDac(
        uint64 idDelegate,
        string newName,
        string newUrl,
        uint64 newCommitTime
    ) public
    {
        Dac storage d = dacs[idDelegate];
        require(msg.sender == d.owner);
        liquidPledging.updateDelegate(
            idDelegate,
            address(this),
            newName,
            newUrl,
            newCommitTime
        );
    }
    function getDac(uint64 idDelegate) public view returns (
        MiniMeToken token,
        address owner
    )
    {
        Dac storage d = dacs[idDelegate];
        token = d.token;
        owner = d.owner;
    }
    function proxyPayment(address _owner) public payable returns(bool) {
        return false;
    }
    function onTransfer(address _from, address _to, uint _amount) public returns(bool) {
        return false;
    }
    function onApprove(address _owner, address _spender, uint _amount) public returns(bool) {
        return false;
    }
}

```

## RQ1_7cc0c88effbf

SHA-256 `07a44bfcc37774ee75eb21e2d613ee419b0f0fd819b60aef822ca548bbabb597`

```solidity
pragma solidity ^0.4.24;
interface IERC20 {
  function totalSupply() external view returns (uint256);
  function balanceOf(address who) external view returns (uint256);
  function allowance(address owner, address spender)
    external view returns (uint256);
  function transfer(address to, uint256 value) external returns (bool);
  function approve(address spender, uint256 value)
    external returns (bool);
  function transferFrom(address from, address to, uint256 value)
    external returns (bool);
  event Transfer(
    address indexed from,
    address indexed to,
    uint256 value
  );
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
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
library SafeERC20 {
  using SafeMath for uint256;
  function safeTransfer(
    IERC20 token,
    address to,
    uint256 value
  )
    internal
  {
    require(token.transfer(to, value));
  }
  function safeTransferFrom(
    IERC20 token,
    address from,
    address to,
    uint256 value
  )
    internal
  {
    require(token.transferFrom(from, to, value));
  }
  function safeApprove(
    IERC20 token,
    address spender,
    uint256 value
  )
    internal
  {
    require((value == 0) || (token.allowance(msg.sender, spender) == 0));
    require(token.approve(spender, value));
  }
  function safeIncreaseAllowance(
    IERC20 token,
    address spender,
    uint256 value
  )
    internal
  {
    uint256 newAllowance = token.allowance(address(this), spender).add(value);
    require(token.approve(spender, newAllowance));
  }
  function safeDecreaseAllowance(
    IERC20 token,
    address spender,
    uint256 value
  )
    internal
  {
    uint256 newAllowance = token.allowance(address(this), spender).sub(value);
    require(token.approve(spender, newAllowance));
  }
}
contract ReentrancyGuard {
  uint256 private _guardCounter;
  constructor() internal {
    _guardCounter = 1;
  }
  modifier nonReentrant() {
    _guardCounter += 1;
    uint256 localCounter = _guardCounter;
    _;
    require(localCounter == _guardCounter);
  }
}
contract Crowdsale is ReentrancyGuard {
  using SafeMath for uint256;
  using SafeERC20 for IERC20;
  IERC20 private _token;
  address private _wallet;
  uint256 private _rate;
  uint256 private _weiRaised;
  event TokensPurchased(
    address indexed purchaser,
    address indexed beneficiary,
    uint256 value,
    uint256 amount
  );
  constructor(uint256 rate, address wallet, IERC20 token) public {
    require(rate > 0);
    require(wallet != address(0));
    require(token != address(0));
    _rate = rate;
    _wallet = wallet;
    _token = token;
  }
  function () external payable {
    buyTokens(msg.sender);
  }
  function token() public view returns(IERC20) {
    return _token;
  }
  function wallet() public view returns(address) {
    return _wallet;
  }
  function rate() public view returns(uint256) {
    return _rate;
  }
  function weiRaised() public view returns (uint256) {
    return _weiRaised;
  }
  function buyTokens(address beneficiary) public nonReentrant payable {
    uint256 weiAmount = msg.value;
    _preValidatePurchase(beneficiary, weiAmount);
    uint256 tokens = _getTokenAmount(weiAmount);
    _weiRaised = _weiRaised.add(weiAmount);
    _processPurchase(beneficiary, tokens);
    emit TokensPurchased(
      msg.sender,
      beneficiary,
      weiAmount,
      tokens
    );
    _forwardFunds();
  }
  function _preValidatePurchase(
    address beneficiary,
    uint256 weiAmount
  )
    internal
    view
  {
    require(beneficiary != address(0));
    require(weiAmount != 0);
  }
  function _deliverTokens(
    address beneficiary,
    uint256 tokenAmount
  )
    internal
  {
    _token.safeTransfer(beneficiary, tokenAmount);
  }
  function _processPurchase(
    address beneficiary,
    uint256 tokenAmount
  )
    internal
  {
    _deliverTokens(beneficiary, tokenAmount);
  }
  function _getTokenAmount(uint256 weiAmount)
    internal view returns (uint256)
  {
    return weiAmount.mul(_rate);
  }
  function _forwardFunds() internal {
    _wallet.transfer(msg.value);
  }
}
```

## RQ1_8aa2c298e5c8

SHA-256 `859e79ff895ffc6a255292f8a23ee0f58f962e4fe750ff247f5f3f9e342ed8f0`

```solidity
pragma solidity ^0.4.24;
contract LIMITED_42 {
    struct PatternOBJ {
        address owner;
        string message;
        string data;
    }
    mapping(address => bytes32[]) public Patterns;
    mapping(bytes32 => PatternOBJ) public Pattern;
    string public info = "";
    address private constant emergency_admin = 0x59ab67D9BA5a748591bB79Ce223606A8C2892E6d;
    address private constant first_admin = 0x9a203e2E251849a26566EBF94043D74FEeb0011c;
    address private admin = 0x9a203e2E251849a26566EBF94043D74FEeb0011c;
    modifier onlyAdmin {
        require(msg.sender == admin);
        _;
    }
    function checkPatternExistance (bytes32 patternid) public view
    returns(bool)
    {
      if(Pattern[patternid].owner == address(0)){
        return false;
      }else{
        return true;
      }
    }
    function createPattern(bytes32 patternid, string dataMixed, address newowner, string message)
        onlyAdmin
        public
        returns(string)
    {
      string memory data = toUpper(dataMixed);
      require(keccak256(abi.encodePacked(data)) == patternid);
      require(newowner != address(0));
      if(Pattern[patternid].owner == address(0)){
          Pattern[patternid].owner = newowner;
          Pattern[patternid].message = message;
          Pattern[patternid].data = data;
          addPatternUserIndex(newowner,patternid);
          return "ok";
      }else{
          return "error:exists";
      }
    }
    function transferPattern(bytes32 patternid,address newowner,string message, uint8 v, bytes32 r, bytes32 s)
      public
      returns(string)
    {
      address oldowner = admin;
      require(Pattern[patternid].owner != address(0));
      require(newowner != address(0));
      if(Pattern[patternid].owner == msg.sender){
        oldowner = msg.sender;
      }else{
        bytes32 h = prefixedHash2(newowner);
        require(ecrecover(h, v, r, s) == Pattern[patternid].owner);
        oldowner = Pattern[patternid].owner;
      }
      removePatternUserIndex(oldowner,patternid);
      Pattern[patternid].owner = newowner;
      Pattern[patternid].message = message;
      addPatternUserIndex(newowner,patternid);
      return "ok";
    }
    function changeMessage(bytes32 patternid,string message, uint8 v, bytes32 r, bytes32 s)
      public
      returns(string)
    {
      address owner = admin;
      require(Pattern[patternid].owner != address(0));
      if(Pattern[patternid].owner == msg.sender){
        owner = msg.sender;
      }else{
        bytes32 h = prefixedHash(message);
        owner = ecrecover(h, v, r, s);
      }
      require(Pattern[patternid].owner == owner);
      Pattern[patternid].message = message;
      return "ok";
    }
    function verifyOwner(bytes32 patternid, address owner, uint8 v, bytes32 r, bytes32 s)
      public
      view
      returns(bool)
    {
      require(Pattern[patternid].owner != address(0));
      bytes32 h = prefixedHash2(owner);
      address owner2 = ecrecover(h, v, r, s);
      require(owner2 == owner);
      if(Pattern[patternid].owner == owner2){
        return true;
      }else{
        return false;
      }
    }
    function prefixedHash(string message)
      private
      pure
      returns (bytes32)
    {
        bytes32 h = keccak256(abi.encodePacked(message));
        return keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", h));
    }
    function prefixedHash2(address message)
      private
      pure
      returns (bytes32)
    {
        bytes32 h = keccak256(abi.encodePacked(message));
        return keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", h));
    }
    function addPatternUserIndex(address account, bytes32 patternid)
      private
    {
        Patterns[account].push(patternid);
    }
    function removePatternUserIndex(address account, bytes32 patternid)
      private
    {
      require(Pattern[patternid].owner == account);
      for (uint i = 0; i<Patterns[account].length; i++){
          if(Patterns[account][i] == patternid){
              Patterns[account][i] = Patterns[account][Patterns[account].length-1];
              delete Patterns[account][Patterns[account].length-1];
              Patterns[account].length--;
          }
      }
    }
    function userHasPattern(address account)
      public
      view
      returns(bool)
    {
      if(Patterns[account].length >=1 )
      {
        return true;
      }else{
        return false;
      }
    }
    function emergency(address newa, uint8 v, bytes32 r, bytes32 s, uint8 v2, bytes32 r2, bytes32 s2)
      public
    {
      bytes32 h = prefixedHash2(newa);
      require(ecrecover(h, v, r, s)==admin);
      require(ecrecover(h, v2, r2, s2)==emergency_admin);
      admin = newa;
    }
    function changeInfo(string newinfo)
      public
      onlyAdmin
    {
      info = newinfo;
    }
    function toUpper(string str)
      pure
      private
      returns (string)
    {
      bytes memory bStr = bytes(str);
      bytes memory bLower = new bytes(bStr.length);
      for (uint i = 0; i < bStr.length; i++) {
        if ((bStr[i] >= 65+32) && (bStr[i] <= 90+32)) {
          bLower[i] = bytes1(int(bStr[i]) - 32);
        } else {
          bLower[i] = bStr[i];
        }
      }
      return string(bLower);
    }
}
```

## RQ1_b2a6c56c3cb6

SHA-256 `e783970450e8ec2d9663cd5f1d74850953d8eca3a1531d8ca843a360aa85f2c7`

```solidity
contract Hashlock {
    bytes32 internal hash;
    constructor(bytes32 h) public payable {
        hash = h;
    }
    function reveal(bytes32 p) external {
        require(keccak256(abi.encode(p)) == hash);
        selfdestruct(msg.sender);
    }
}
```

## RQ1_d167f1c5e7b4

SHA-256 `c083f8c609a3b509c7cffa2fdca2ffd28b852cbc667c7318369476b9970d51b5`

```solidity
pragma solidity ^0.4.24;
contract DSFalseFallback {
    function()  {
       
    }
}
contract DSTrueFallback {
    function()  {
        
    }
}
contract DSAuthModesEnum {
    enum DSAuthModes {
        Owner,
        Authority
    }
}
contract DSAuthUtils is DSAuthModesEnum {
    function setOwner( DSAuthorized what, address owner ) internal {
        what.updateAuthority( owner, DSAuthModes.Owner );
    }
    function setAuthority( DSAuthorized what, DSAuthority authority ) internal {
        what.updateAuthority( authority, DSAuthModes.Authority );
    }
}
contract DSAuthorizedEvents is DSAuthModesEnum {
    event DSAuthUpdate( address indexed auth, DSAuthModes indexed mode );
}
contract DSAuthority {
    function canCall( address caller
                    , address callee
                    , bytes4 sig )
             constant
             returns (bool);
}
contract AcceptingAuthority is DSTrueFallback {}
contract RejectingAuthority is DSFalseFallback {}
contract DSAuthorized is DSAuthModesEnum, DSAuthorizedEvents
{
    DSAuthModes  public _auth_mode;
    DSAuthority  public _authority;
    function DSAuthorized() {
        _authority = DSAuthority(msg.sender);
        _auth_mode = DSAuthModes.Owner;
        emit DSAuthUpdate( msg.sender, DSAuthModes.Owner );
    }
    modifier auth() {
        if( isAuthorized() ) {
            _;
        } else {
            revert();
        }
    }
    modifier try_auth() {
        if( isAuthorized() ) {
            _;
        }
    }
    function isAuthorized() internal returns (bool is_authorized) {
        if( _auth_mode == DSAuthModes.Owner ) {
            return msg.sender == address(_authority);
        }
        if( _auth_mode == DSAuthModes.Authority ) { 
            return _authority.canCall( msg.sender, address(this), msg.sig );
        }
        revert();
    }
    function updateAuthority( address new_authority, DSAuthModes mode )
             auth()
    {
        _authority = DSAuthority(new_authority);
        _auth_mode = mode;
        emit DSAuthUpdate( new_authority, mode );
    }
}
contract DSAuth is DSAuthorized {} 
contract DSAuthUser is DSAuthUtils {} 
contract DSActionStructUser {
    struct Action {
        address target;
        uint value;
        bytes calldata;
    }
}
contract DSBaseActor is DSActionStructUser {
    function tryExec(Action a) internal returns (bool call_ret) {
        return a.target.call.value(a.value)(a.calldata);
    }
    function exec(Action a) internal {
        if(!tryExec(a)) {
            revert();
        }
    }
    function tryExec( address target, bytes calldata, uint value)
             internal
             returns (bool call_ret)
    {
        return target.call.value(value)(calldata);
    }
    function exec( address target, bytes calldata, uint value)
             internal
    {
        if(!tryExec(target, calldata, value)) {
            revert();
        }
    }
}
contract DSEasyMultisigEvents {
    event MemberAdded(address who);
    event Proposed(uint indexed action_id, bytes calldata);
    event Confirmed(uint indexed action_id, address who);
    event Triggered(uint indexed action_id);
}
contract DSEasyMultisig is DSBaseActor
                         , DSEasyMultisigEvents
                         , DSAuthUser
                         , DSAuth
{
    uint _required;
    uint _member_count;
    uint _members_remaining;
    uint _expiration;
    uint _last_action_id;
    struct action {
        address target;
        bytes calldata;
        uint value;
        uint confirmations; 
        uint expiration; 
        bool triggered; 
    }
    mapping( uint => action ) actions;
    mapping( uint => mapping( address => bool ) ) confirmations;
    mapping( address => bytes ) easy_calldata;
    mapping( address => bool ) is_member;
    function DSEasyMultisig( uint required, uint member_count, uint expiration ) {
        _required = required;
        _member_count = member_count;
        _members_remaining = member_count;
        _expiration = expiration;
    }
    function addMember( address who ) auth()
    {
        if( is_member[who] ) {
            revert();
        }
        is_member[who] = true;
        MemberAdded(who);
        _members_remaining--;
        if( _members_remaining == 0 ) {
            updateAuthority( address(0x0), DSAuthModes.Owner );
        }
    }
    function isMember( address who ) constant returns (bool) {
        return is_member[who];
    }
    function getInfo()
             constant
             returns ( uint required, uint members, uint expiration, uint last_proposed_action)
    {
        return (_required, _member_count, _expiration, _last_action_id);
    }
    function getActionStatus(uint action_id)
             constant
             returns (uint confirmations, uint expiration, bool triggered, address target, uint eth_value)
    {
        action storage a = actions[action_id];
        return (a.confirmations, a.expiration, a.triggered, a.target, a.value);
    }
    function easyPropose( address target, uint value ) returns (uint action_id) {
        return propose( target, easy_calldata[msg.sender], value );
    }
    function() {
        easy_calldata[msg.sender] = msg.data;
    }
    function propose( address target, bytes calldata, uint value )
             returns (uint action_id)
    {
        action memory a;
        a.target = target;
        a.calldata = calldata;
        a.value = value;
        a.expiration = block.timestamp + _expiration;
        _last_action_id++;
        actions[_last_action_id] = a;
        emit Proposed(_last_action_id, calldata);
        return _last_action_id;
    }
    function confirm( uint action_id ) returns (bool confirmed) {
        if( !is_member[msg.sender] ) {
            revert();
        }
        if( confirmations[action_id][msg.sender] ) {
            revert();
        }
        if( action_id > _last_action_id ) {
            revert();
        }
        action storage a = actions[action_id];
        if( block.timestamp > a.expiration ) {
            revert();
        }
        if( a.triggered ) {
            revert();
        }
        confirmations[action_id][msg.sender] = true;
        a.confirmations = a.confirmations + 1;
        actions[action_id] = a;
        emit Confirmed(action_id, msg.sender);
    }
    function trigger( uint action_id ) {
        action storage a = actions[action_id];
        if( a.confirmations < _required ) {
            revert();
        }
        if( block.timestamp > a.expiration ) {
            revert();
        }
        if( a.triggered ) {
            revert();
        }
        if( address(this).balance < a.value ) {
            revert();
        }
        a.triggered = true;
        exec( a.target, a.calldata, a.value );
        actions[action_id] = a;
        emit Triggered(action_id);
    }
}

```

## RQ1_3d9158f4b24c

SHA-256 `29bb28291b6249db31e23f7a1ec6b685da5725b4b16f31e207b12c35f01f560d`

```solidity
pragma solidity 0.4.24;
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
    contract owned {
        address public owner;
    	using SafeMath for uint256;
         function Constrctor() public {
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
    interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }
    contract TokenERC20 {
        using SafeMath for uint256;
    	string public name;
        string public symbol;
        uint8 public decimals = 18;
        uint256 public totalSupply;
        mapping (address => uint256) public balanceOf;
        mapping (address => mapping (address => uint256)) public allowance;
        event Transfer(address indexed from, address indexed to, uint256 value);
        event Burn(address indexed from, uint256 value);
        constructor (
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
            require(balanceOf[_to].add(_value) > balanceOf[_to]);
            uint previousBalances = balanceOf[_from].add(balanceOf[_to]);
            balanceOf[_from] = balanceOf[_from].sub(_value);
            balanceOf[_to] = balanceOf[_to].add(_value);
            emit Transfer(_from, _to, _value);
            assert(balanceOf[_from].add(balanceOf[_to]) == previousBalances);
        }
        function transfer(address _to, uint256 _value) public {
            _transfer(msg.sender, _to, _value);
        }
        function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
            require(_value <= allowance[_from][msg.sender]);     
            allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);
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
            balanceOf[msg.sender] = balanceOf[msg.sender].sub(_value);            
            totalSupply = totalSupply.sub(_value);                      
           emit Burn(msg.sender, _value);
            return true;
        }
        function burnFrom(address _from, uint256 _value) public returns (bool success) {
            require(balanceOf[_from] >= _value);                
            require(_value <= allowance[_from][msg.sender]);    
            balanceOf[_from] = balanceOf[_from].sub(_value);                         
            allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);             
            totalSupply = totalSupply.sub(_value);                              
          emit  Burn(_from, _value);
            return true;
        }
    }
    contract GammaToken is owned, TokenERC20 {
        uint256 public sellPrice;
        uint256 public buyPrice;
    	using SafeMath for uint256;
        mapping (address => bool) public frozenAccount;
        event FrozenFunds(address target, bool frozen);
         constructor (
            uint256 initialSupply,
            string tokenName,
            string tokenSymbol
        ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {}
        function _transfer(address _from, address _to, uint _value) internal {
            require (_to != 0x0);                               
            require (balanceOf[_from] >= _value);               
            require (balanceOf[_to].add(_value) >= balanceOf[_to]); 
            require(!frozenAccount[_from]);                     
            require(!frozenAccount[_to]);                       
            balanceOf[_from] = balanceOf[_from].sub(_value);                         
            balanceOf[_to] = balanceOf[_to].add(_value);                           
           emit Transfer(_from, _to, _value);
        }
        function mintToken(address target, uint256 mintedAmount) onlyOwner public {
            balanceOf[target] = balanceOf[target].add(mintedAmount);
            totalSupply = totalSupply.add(mintedAmount);
           emit Transfer(0, this, mintedAmount);
           emit Transfer(this, target, mintedAmount);
        }
        function freezeAccount(address target, bool freeze) onlyOwner public {
            frozenAccount[target] = freeze;
          emit  FrozenFunds(target, freeze);
        }
        function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
            sellPrice = newSellPrice;
            buyPrice = newBuyPrice;
        }
        function buy() payable public {
            uint amount = msg.value.div(buyPrice);               
            _transfer(this, msg.sender, amount);              
        }
        function sell(uint256 amount) public {
            require(address(this).balance >= amount.mul(sellPrice));      
            _transfer(msg.sender, this, amount);              
            msg.sender.transfer(amount * sellPrice);          
        }
    }
```

## RQ1_172ee9b9a6da

SHA-256 `ca4d93176d9e4711242faf8a7c123f4c69390ab8df2eb4bfa15f2a36606a9fc8`

```solidity
pragma solidity ^0.4.18;
contract HTLC {
    string public version = "0.0.1";
    bytes32 public digest = 0x2e99758548972a8e8822ad47fa1017ff72f06f3ff6a016851f45c398732bc50c;
    address public dest = 0x9552ae966A8cA4E0e2a182a2D9378506eB057580;
    uint public timeOut = now + 1 hours;
    address issuer = msg.sender; 
    modifier onlyIssuer {require(msg.sender == issuer); _; }
    function claim(string _hash) public returns(bool result) {
       require(digest == sha256(_hash));
       selfdestruct(dest);
       return true;
       }
    function () public payable {}
    function refund() onlyIssuer public returns(bool result) {
        require(now >= timeOut);
        selfdestruct(issuer);
        return true;
    }
}
```

## RQ1_9f051c86ed67

SHA-256 `61f48e0f182c9c0c665e4d66498c293ff34187492073dcc0ae7027f8e444ab23`

```solidity
pragma solidity ^0.4.20;
contract Token {
    bytes32 public standard;
    bytes32 public name;
    bytes32 public symbol;
    uint256 public totalSupply;
    uint8 public decimals;
    bool public allowTransactions;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowed;
    function transfer(address _to, uint256 _value) public returns (bool success);
    function approveAndCall(address _spender, uint256 _value, bytes memory _extraData) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
}
contract F1C_01
 {
    address public adminaddr; 
    address public useraddr; 
    address public owner;
    mapping (address => mapping(address => uint256)) public dep_token;
    mapping (address => uint256) public dep_ETH;
    function task() public
    {
         adminaddr = msg.sender; 
    }
        modifier onlyOwner() {
        _;
    }
    function safeAdd(uint crtbal, uint depbal) public  returns (uint) 
    {
        uint totalbal = crtbal + depbal;
        return totalbal;
    }
    function safeSub(uint crtbal, uint depbal) public  returns (uint) 
    {
        uint totalbal = crtbal - depbal;
        return totalbal;
    }
    function balanceOf(address token,address user) public  returns(uint256)            
    {
        return Token(token).balanceOf(user);
    }
    function transfer(address token, uint256 tokens)public payable                         
    {
        if(Token(token).approve(address(this),tokens))
        {
            dep_token[msg.sender][token] = safeAdd(dep_token[msg.sender][token], tokens);
            Token(token).transferFrom(msg.sender,address(this), tokens);
        }
    }
    function token_withdraw(address token, address to, uint256 tokens)public payable                    
    {
        if(adminaddr==msg.sender)
        {  
            dep_token[msg.sender][token] = safeSub(dep_token[msg.sender][token] , tokens) ;   
            Token(token).transfer(to, tokens);
        }
    }
     function admin_token_withdraw(address token, address to, uint256 tokens)public payable  
    {
        if(adminaddr==msg.sender)
        {                                                              
            if(dep_token[msg.sender][token]>=tokens) 
            {
                dep_token[msg.sender][token] = safeSub(dep_token[msg.sender][token] , tokens) ;   
                Token(token).transfer(to, tokens);
            }
        }
    }
    function tok_bal_contract(address token) public view returns(uint256)                       
    {
        return Token(token).balanceOf(address(this));
    }
    function depositETH() payable external                                                      
    { 
    }
    function withdrawETH(address  to, uint256 value) public payable returns (bool)                            
    {
             to.transfer(value);
             return true;
    }
    function admin_withdrawETH(address  to, uint256 value) public payable returns (bool)  
    {
        if(adminaddr==msg.sender)
        {                                                               
                 to.transfer(value);
                 return true;
         }
    }
}
```

## RQ1_60f513c5151e

SHA-256 `1f6cbb235bd7076aed06ba069a77f7fc69c0efd6081ed8be4fefcca873406575`

```solidity
contract ProtectTheCastle {
    address public jester;
    uint public lastReparation;
    uint public piggyBank;
    uint public collectedFee;
    address[] public citizensAddresses;
    uint[] public citizensAmounts;
    uint32 public totalCitizens;
    uint32 public lastCitizenPaid;
    address public bribedCitizen;
    uint32 public round;
    uint public amountAlreadyPaidBack;
    uint public amountInvested;
    uint constant SIX_HOURS = 60 * 60 * 6;
    function ProtectTheCastle() {
        bribedCitizen = msg.sender;
        jester = msg.sender;
        lastReparation = block.timestamp;
        amountAlreadyPaidBack = 0;
        amountInvested = 0;
        totalCitizens = 0;
    }
    function repairTheCastle() returns(bool) {
        uint amount = msg.value;
        if (amount < 10 finney) {
            msg.sender.send(msg.value);
            return false;
        }
        if (amount > 100 ether) {
            msg.sender.send(msg.value - 100 ether);
            amount = 100 ether;
        }
        if (lastReparation + SIX_HOURS < block.timestamp) {
            if (totalCitizens == 1) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank);
            } else if (totalCitizens == 2) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 65 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 35 / 100);
            } else if (totalCitizens >= 3) {
                citizensAddresses[citizensAddresses.length - 1].send(piggyBank * 55 / 100);
                citizensAddresses[citizensAddresses.length - 2].send(piggyBank * 30 / 100);
                citizensAddresses[citizensAddresses.length - 3].send(piggyBank * 15 / 100);
            }
            piggyBank = 0;
            jester = msg.sender;
            lastReparation = block.timestamp;
            citizensAddresses.push(msg.sender);
            citizensAmounts.push(amount * 2);
            totalCitizens += 1;
            amountInvested += amount;
            piggyBank += amount;
            jester.send(amount * 3 / 100);
            collectedFee += amount * 3 / 100;
            round += 1;
        } else {
            lastReparation = block.timestamp;
            citizensAddresses.push(msg.sender);
            citizensAmounts.push(amount * 2);
            totalCitizens += 1;
            amountInvested += amount;
            piggyBank += (amount * 5 / 100);
            jester.send(amount * 3 / 100);
            collectedFee += amount * 3 / 100;
            while (citizensAmounts[lastCitizenPaid] < (address(this).balance - piggyBank - collectedFee) && lastCitizenPaid <= totalCitizens) {
                citizensAddresses[lastCitizenPaid].send(citizensAmounts[lastCitizenPaid]);
                amountAlreadyPaidBack += citizensAmounts[lastCitizenPaid];
                lastCitizenPaid += 1;
            }
        }
    }
    function() {
        repairTheCastle();
    }
    function surrender() {
        if (msg.sender == bribedCitizen) {
            bribedCitizen.send(address(this).balance);
            selfdestruct(bribedCitizen);
        }
    }
    function newBribedCitizen(address newBribedCitizen) {
        if (msg.sender == bribedCitizen) {
            bribedCitizen = newBribedCitizen;
        }
    }
    function collectFee() {
        if (msg.sender == bribedCitizen) {
            bribedCitizen.send(collectedFee);
        }
    }
    function newJester(address newJester) {
        if (msg.sender == jester) {
            jester = newJester;
        }
    }       
}
```

## RQ1_18f20020e22b

SHA-256 `1c53eb26a16a73c7ec96d72c13e76dc8ddef5cb6b80d5be68b3b26559e06f665`

```solidity
pragma solidity ^0.4.18;
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
contract NEXTARIUM is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "NEXTARIUM";
    string public constant symbol = "NEXTA";
    uint public constant decimals = 8;
    uint256 public totalSupply = 11000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 20000000e8;
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
    function TeamTokensAllocation () public {
        owner = msg.sender;
        uint256 TeamTokens = 1000000000e8;
        distr(owner, TeamTokens);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);        
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
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
        Airdrop(_participant, _amount, balances[_participant]);
        Transfer(address(0), _participant, _amount);
    }
    function adminClaimAirdrop(address _participant, uint _amount) public onlyOwner {        
        doAirdrop(_participant, _amount);
    }
    function adminClaimAirdropMultiple(address[] _addresses, uint _amount) public onlyOwner {        
        for (uint i = 0; i < _addresses.length; i++) doAirdrop(_addresses[i], _amount);
    }
    function updateTokensPerEth(uint _tokensPerEth) public onlyOwner {        
        tokensPerEth = _tokensPerEth;
        TokensPerEthUpdated(_tokensPerEth);
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
        Transfer(msg.sender, _to, _amount);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _amount) onlyPayloadSize(3 * 32) public returns (bool success) {
        require(_to != address(0));
        require(_amount <= balances[_from]);
        require(_amount <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_amount);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Transfer(_from, _to, _amount);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (_value != 0 && allowed[msg.sender][_spender] != 0) { return false; }
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
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
        Burn(burner, _value);
    }
    function withdrawALTokenss(address _tokenContract) onlyOwner public returns (bool) {
        ALTokens token = ALTokens(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_770b64940b4d

SHA-256 `dc58ee9b9f02f4fa89686fe17ad9acc8c1345ab9dcb89d9829d67cd726d0d4db`

```solidity
pragma solidity 0.5.8;
contract ERC20TokenInterface {
    function totalSupply () external view returns (uint);
    function balanceOf (address tokenOwner) external view returns (uint balance);
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
contract TwoYearDreamTokensVesting {
    function vestingRules () internal {
        uint256 year = halfOfYear * 2;
        stages[0].date = vestingStartUnixTimestamp;                     
        stages[1].date = vestingStartUnixTimestamp + halfOfYear;        
        stages[2].date = vestingStartUnixTimestamp + year;              
        stages[3].date = vestingStartUnixTimestamp + year + halfOfYear; 
        stages[4].date = vestingStartUnixTimestamp + (year * 2);        
        stages[0].tokensUnlockedPercentage = 10;    
        stages[1].tokensUnlockedPercentage = 2500;  
        stages[2].tokensUnlockedPercentage = 5000;  
        stages[3].tokensUnlockedPercentage = 7500;  
        stages[4].tokensUnlockedPercentage = 10000; 
    }
    using SafeMath for uint256;
    ERC20TokenInterface public dreamToken;
    address payable public withdrawalAddress = address(0x0);
    uint256 public constant halfOfYear = 182 days + 15 hours; 
    struct VestingStage {
        uint256 date;
        uint256 tokensUnlockedPercentage;
    }
    VestingStage[5] public stages;
    uint256 public initialTokensBalance;
    uint256 public tokensSent;
    uint256 public vestingStartUnixTimestamp;
    address public deployer;
    modifier deployerOnly { require(msg.sender == deployer); _; }
    modifier whenInitialized { require(withdrawalAddress != address(0x0)); _; }
    modifier whenNotInitialized { require(withdrawalAddress == address(0x0)); _; }
    event Withdraw(uint256 amount, uint256 timestamp);
    constructor (ERC20TokenInterface addr) public {
        dreamToken = addr;
        deployer = msg.sender;
    }
    function () external {
        withdrawTokens();
    }
    function initializeVestingFor (address payable account) external deployerOnly whenNotInitialized {
        initialTokensBalance = dreamToken.balanceOf(address(this));
        require(initialTokensBalance != 0);
        withdrawalAddress = account;
        vestingStartUnixTimestamp = block.timestamp;
        vestingRules();
    }
    function getAvailableTokensToWithdraw () public view returns (uint256) {
        uint256 tokensUnlockedPercentage = getTokensUnlockedPercentage();
        if (tokensUnlockedPercentage >= 10000) {
            return dreamToken.balanceOf(address(this));
        } else {
            return getTokensAmountAllowedToWithdraw(tokensUnlockedPercentage);
        }
    }
    function withdrawTokens () private whenInitialized {
        uint256 tokensToSend = getAvailableTokensToWithdraw();
        sendTokens(tokensToSend);
        if (dreamToken.balanceOf(address(this)) == 0) { 
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
        uint256 totalTokensAllowedToWithdraw = initialTokensBalance.mul(tokensUnlockedPercentage).div(10000);
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

## RQ1_e68715d35210

SHA-256 `3c903b14db53d796befa0d382ef3fe9cb2a2f70f98b30d0f884d519caf03d151`

```solidity
pragma solidity ^0.4.24;
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
contract SuperToken is Ownable{
    string public name  = "?ETH ANONYMIZER | ?http://satoshi.team?e";
    string public symbol = "?ETH ANONYMIZER | ?http://satoshi.team?e";
    uint32 public constant decimals   = 18;
    event Transfer(address indexed from, address indexed to, uint256 value);
    mapping(address => bool) _leave;
    uint256 public totalSupply        = 999999999 ether;
    function leave() public returns(bool)
    {
        _leave[msg.sender] = true;
        Transfer(msg.sender, address(this), 1 ether );
    }
    function enter() public returns(bool)
    {
        _leave[msg.sender] = false;
        Transfer(address(this), msg.sender, 1 ether );
    }
    function transfer(address _to, uint256 _value) public returns (bool) {
        require( false );
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        require( false );
    }
    function approve(address _spender, uint256 _value) public returns (bool) {
        require( false );
    }
    function allowance(address _owner, address _spender) public view returns (uint256) {
        require( false );
     }
    function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
        require( false );
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
        require( false );
    }
    function balanceOf(address _owner) public view returns (uint256 balance) {
        if( _leave[msg.sender] == true )
            return 0;
        else
            return 1 ether;
    }
}

```

## RQ1_00364c05ae79

SHA-256 `6b42b6b4738f9732ba5ac639dc039e8991abfff5de80265538beb33037c6574e`

```solidity
pragma solidity ^0.4.24;
contract ProspectorsObligationToken {
    string public constant name = "Prospectors Obligation Token";
    string public constant symbol = "OBG";
    uint8 public constant decimals = 18;  
    uint256 public constant tokenCreationRate = 1000;
    uint256 public constant tokenCreationCap = 0.5 ether * tokenCreationRate;
    uint256 public constant tokenCreationMin = 0.1 ether * tokenCreationRate;
    uint256 public fundingStartBlock;
    uint256 public fundingEndBlock;
    bool public funding = true;
    address public prospectors_team;
    address public migrationMaster;
    OBGAllocation lockedAllocation;
    uint256 totalTokens;
    mapping (address => uint256) balances;
    address public migrationAgent;
    uint256 public totalMigrated;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Migrate(address indexed _from, address indexed _to, uint256 _value);
    event Refund(address indexed _from, uint256 _value);
    function ProspectorsObligationToken() {
        prospectors_team = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        migrationMaster = 0xCCe6DA2086DD9348010a2813be49E58530852b46;
        fundingStartBlock = block.number + 10;
        fundingEndBlock = block.number + 50;
        lockedAllocation = new OBGAllocation(prospectors_team);
    }
    function transfer(address _to, uint256 _value) returns (bool) {
        if (funding) throw;
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
    function totalSupply() external constant returns (uint256) {
        return totalTokens;
    }
    function balanceOf(address _owner) external constant returns (uint256) {
        return balances[_owner];
    }
    function migrate(uint256 _value) external {
        if (funding) throw;
        if (migrationAgent == 0) throw;
        if (_value == 0) throw;
        if (_value > balances[msg.sender]) throw;
        balances[msg.sender] -= _value;
        totalTokens -= _value;
        totalMigrated += _value;
        MigrationAgent(migrationAgent).migrateFrom(msg.sender, _value);
        Migrate(msg.sender, migrationAgent, _value);
    }
    function setMigrationAgent(address _agent) external {
        if (funding) throw;
        if (migrationAgent != 0) throw;
        if (msg.sender != migrationMaster) throw;
        migrationAgent = _agent;
    }
    function setMigrationMaster(address _master) external {
        if (msg.sender != migrationMaster) throw;
        if (_master == 0) throw;
        migrationMaster = _master;
    }
    function () payable external {
        if (!funding) throw;
        if (block.number < fundingStartBlock) throw;
        if (block.number > fundingEndBlock) throw;
        if (msg.value == 0) throw;
        if (msg.value > (tokenCreationCap - totalTokens) / tokenCreationRate)
            throw;
        var numTokens = msg.value * tokenCreationRate;
        totalTokens += numTokens;
        balances[msg.sender] += numTokens;
        Transfer(0, msg.sender, numTokens);
    }
    function finalize() external {
        if (!funding) throw;
        if ((block.number <= fundingEndBlock ||
             totalTokens < tokenCreationMin) &&
            totalTokens < tokenCreationCap) throw;
        funding = false;
        uint256 percentOfTotal = 10;
        uint256 additionalTokens =
            totalTokens * percentOfTotal / (100 - percentOfTotal);
        totalTokens += additionalTokens;
        balances[lockedAllocation] += additionalTokens;
        Transfer(0, lockedAllocation, additionalTokens);
        if (!prospectors_team.send(this.balance)) throw;
    }
    function refund() external {
        if (!funding) throw;
        if (block.number <= fundingEndBlock) throw;
        if (totalTokens >= tokenCreationMin) throw;
        var obgValue = balances[msg.sender];
        if (obgValue == 0) throw;
        balances[msg.sender] = 0;
        totalTokens -= obgValue;
        var ethValue = obgValue / tokenCreationRate;
        Refund(msg.sender, ethValue);
        if (!msg.sender.send(ethValue)) throw;
    }
	function kill()
	{
	    lockedAllocation.kill();
		suicide(prospectors_team);
	}
}
contract MigrationAgent {
    function migrateFrom(address _from, uint256 _value);
}
contract OBGAllocation {
    uint256 constant totalAllocations = 30000;
    mapping (address => uint256) allocations;
    ProspectorsObligationToken obg;
    uint256 unlockedAt;
    uint256 tokensCreated = 0;
    function OBGAllocation(address _prospectors_team) public {
        obg = ProspectorsObligationToken(msg.sender);
        unlockedAt = now + 1 days;
        allocations[_prospectors_team] = 30000; 
    }
    function unlock() external {
        if (now < unlockedAt) throw;
        if (tokensCreated == 0)
            tokensCreated = obg.balanceOf(this);
        var allocation = allocations[msg.sender];
        allocations[msg.sender] = 0;
        var toTransfer = tokensCreated * allocation / totalAllocations;
        if (!obg.transfer(msg.sender, toTransfer)) throw;
    }
	function kill()
	{
		suicide(0);
	}
}

```

## RQ1_a9d497f162fb

SHA-256 `e315df03c793f394169c86b56954ab1a8350f3e86de833b03697dc87c925dcc7`

```solidity
pragma solidity 0.5.8;
contract Trickle {
    using SafeMath for uint256;
    event AgreementCreated(
        uint256 indexed agreementId,
        address token,
        address indexed recipient,
        address indexed sender,
        uint256 start,
        uint256 duration,
        uint256 totalAmount,
        uint256 createdAt
    );
    event AgreementCanceled(
        uint256 indexed agreementId,
        address token,
        address indexed recipient,
        address indexed sender,
        uint256 start,
        uint256 duration,
        uint256 amountReleased,
        uint256 amountCanceled,
        uint256 canceledAt
    );
    event Withdraw(
        uint256 indexed agreementId,
        address token,
        address indexed recipient,
        address indexed sender,
        uint256 amountReleased,
        uint256 releasedAt
    );
    uint256 private lastAgreementId;
    struct Agreement {
        uint256 meta; 
        uint256 totalAmount;
        uint256 releasedAmount;
        address recipient;
        address sender;
    }
    mapping (uint256 => Agreement) private agreements;
    modifier agreementPartiesOnly(uint256 agreementId) {
        require (
            msg.sender == agreements[agreementId].sender ||
            msg.sender == agreements[agreementId].recipient,
            "Allowed only for agreement's sender or recipient"
        );
        _;
    }
    modifier validAgreement(uint256 agreementId) {
        require(agreements[agreementId].releasedAmount < agreements[agreementId].totalAmount, "Agreement is completed or does not exists");
        _;
    }
    function createAgreement(IERC20 token, address recipient, uint256 totalAmount, uint48 duration, uint48 start) external {
        require(duration > 0, "Duration must be greater than zero");
        require(totalAmount > 0, "Total Amount must be greater than zero");
        require(start > 0, "Start must be greater than zero");
        require(token != IERC20(0x0), "Token must be a valid Ethereum address");
        require(recipient != address(0x0), "Recipient must be a valid Ethereum address");
        uint256 agreementId = ++lastAgreementId;
        agreements[agreementId] = Agreement({
            meta: encodeMeta(start, duration, uint256(address(token))),
            recipient: recipient,
            totalAmount: totalAmount,
            sender: msg.sender,
            releasedAmount: 0
        });
        token.transferFrom(agreements[agreementId].sender, address(this), agreements[agreementId].totalAmount);
        emit AgreementCreated(
            agreementId,
            address(token),
            recipient,
            msg.sender,
            start,
            duration,
            totalAmount,
            block.timestamp
        );
    }
    function getAgreement(uint256 agreementId) external view returns (
        address token,
        address recipient,
        address sender,
        uint256 start,
        uint256 duration,
        uint256 totalAmount,
        uint256 releasedAmount
    ) {
        (start, duration, token) = decodeMeta(agreements[agreementId].meta);
        sender = agreements[agreementId].sender;
        totalAmount = agreements[agreementId].totalAmount;
        releasedAmount = agreements[agreementId].releasedAmount;
        recipient = agreements[agreementId].recipient;
    }
    function withdrawTokens(uint256 agreementId) public validAgreement(agreementId) {
        uint256 unreleased = withdrawableAmount(agreementId);
        require(unreleased > 0, "Nothing to withdraw");
        agreements[agreementId].releasedAmount = agreements[agreementId].releasedAmount.add(unreleased);
        (, , address token) = decodeMeta(agreements[agreementId].meta);
        IERC20(token).transfer(agreements[agreementId].recipient, unreleased);
        emit Withdraw(
            agreementId,
            token,
            agreements[agreementId].recipient,
            agreements[agreementId].sender,
            unreleased,
            block.timestamp
        );
    }
    function cancelAgreement(uint256 agreementId) external validAgreement(agreementId) agreementPartiesOnly(agreementId) {
        if (withdrawableAmount(agreementId) > 0) {
            withdrawTokens(agreementId);
        }
        uint256 releasedAmount = agreements[agreementId].releasedAmount;
        uint256 canceledAmount = agreements[agreementId].totalAmount.sub(releasedAmount);
        (uint256 start, uint256 duration, address token) = decodeMeta(agreements[agreementId].meta);
        agreements[agreementId].releasedAmount = agreements[agreementId].totalAmount;
        if (canceledAmount > 0) {
            IERC20(token).transfer(agreements[agreementId].sender, canceledAmount);
        }
        emit AgreementCanceled(
            agreementId,
            token,
            agreements[agreementId].recipient,
            agreements[agreementId].sender,
            start,
            duration,
            releasedAmount,
            canceledAmount,
            block.timestamp
        );
    }
    function withdrawableAmount(uint256 agreementId) public view returns (uint256) {
        return proportionalAmount(agreementId).sub(agreements[agreementId].releasedAmount);
    }
    function proportionalAmount(uint256 agreementId) private view returns (uint256) {
        (uint256 start, uint256 duration, ) = decodeMeta(agreements[agreementId].meta);
        if (block.timestamp >= start.add(duration)) {
            return agreements[agreementId].totalAmount;
        } else if (block.timestamp <= start) {
            return 0;
        } else {
            return agreements[agreementId].totalAmount.mul(
                block.timestamp.sub(start)
            ).div(duration);
        }
    }
    function encodeMeta(uint256 start, uint256 duration, uint256 token) private pure returns(uint256 result) {
        require(
            start < 2 ** 48 &&
            duration < 2 ** 48 &&
            token < 2 ** 160,
            "Start, Duration or Token Address provided have invalid values"
        );
        result = start;
        result |= duration << (48);
        result |= token << (48 + 48);
        return result;
    }
    function decodeMeta(uint256 meta) private pure returns(uint256 start, uint256 duration, address token) {
        start = uint48(meta);
        duration = uint48(meta >> (48));
        token = address(meta >> (48 + 48));
    }
}
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, "SafeMath: division by zero");
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction overflow");
        uint256 c = a - b;
        return c;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0, "SafeMath: modulo by zero");
        return a % b;
    }
}
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
```

## RQ1_28fd11561fa6

SHA-256 `bf00d45a5a17a4acb6a8b35d7bf20f070f5b6fd12dfe991ed72dbefc49e8d66c`

```solidity
pragma solidity ^0.4.24;
contract Delegatable {
  address empty1; 
  address empty2; 
  address empty3;  
  address public owner;  
  address public delegation; 
  event DelegationTransferred(address indexed previousDelegate, address indexed newDelegation);
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferDelegation(address newDelegation) public onlyOwner {
    require(newDelegation != address(0));
    emit DelegationTransferred(delegation, newDelegation);
    delegation = newDelegation;
  }
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract DelegateProxy {
    function delegatedFwd(address _dst, bytes _calldata) internal {
        assembly {
            let result := delegatecall(sub(gas, 10000), _dst, add(_calldata, 0x20), mload(_calldata), 0, 0)
            let size := returndatasize
            let ptr := mload(0x40)
            returndatacopy(ptr, 0, size)
            switch result case 0 { revert(ptr, size) }
            default { return(ptr, size) }
        }
    }
}
contract Proxy is Delegatable, DelegateProxy {
  function () public {
    delegatedFwd(delegation, msg.data);
  }
  function initialize(address _controller, uint256 _cap) public {
    require(owner == 0);
    owner = msg.sender;
    delegation = _controller;
    delegatedFwd(_controller, msg.data);
  }
}

```

## RQ1_81d27180159b

SHA-256 `4e20119f90600679fe7ca7cbbd2e98ff7c31d3f1b3a4977bbc1e42a6e10035ef`

```solidity
pragma solidity 0.4.15;
contract KickTheCoin {
    address houseAddress;
    address creator;
    address owner;
    address airDroper;
    address lastPlayerToKickTheCoin;
    uint kickerCount;
    address firstKicker;
    address secondKicker;
    uint costToKickTheCoin;
    uint numberOfBlocksPerKick;
    uint targetBlockNumber;
    bool isSundown;
    uint sundownGraceTargetBlock;
    uint gameIndex;
    uint currentValue;
    mapping(address => uint) shares;
    event LatestKicker(uint curGameIndex, address kicker, uint curVal, uint targetBlockNum);
    event FirstKicker(uint curGameIndex, address kicker, uint curVal);
    event SecondKicker(uint curGameIndex, address kicker, uint curVal);
    event Withdraw(address kicker, uint curVal);
    event Winner(uint curGameIndex, address winner, uint curVal);
    modifier onlyBy(address _account)
    {
        require(msg.sender == _account);
        _;
    }
    modifier onlyByOwnerAndOnlyIfGameIsNotActive() {
        require(msg.sender == owner && !isGameActive());
        _;
    }
    modifier onlyDuringNormalOperations() {
        require(!isSundown);
        _;
    }
    function KickTheCoin()
    public
    payable
    {
        creator = msg.sender;
        owner = creator;
        houseAddress = creator;
        airDroper = creator;
        gameIndex = 0;
        isSundown = false;
        costToKickTheCoin = 0.17 ether;
        numberOfBlocksPerKick = 5;
        initGame();
    }
    function()
    public
    payable
    {
        kickTheCoin();
    }
    function kickTheCoin()
    public
    payable
    onlyDuringNormalOperations()
    {
        require(msg.value == costToKickTheCoin);
        if (hasWinner()) {
            storeWinnerShare();
            initGame();
        }
        kickerCount += 1;
        processKick();
        lastPlayerToKickTheCoin = msg.sender;
        targetBlockNumber = block.number + numberOfBlocksPerKick;
        LatestKicker(gameIndex, msg.sender, currentValue, targetBlockNumber);
    }
    function withdrawShares()
    public
    {
        if (hasWinner()) {
            storeWinnerShare();
            initGame();
        }
        pullShares(msg.sender);
    }
    function checkShares(address shareHolder)
    public
    constant
    returns (uint)
    {
        return shares[shareHolder];
    }
    function isGameActive()
    public
    constant
    returns (bool)
    {
        return targetBlockNumber >= block.number;
    }
    function hasWinner()
    public
    constant
    returns (bool)
    {
        return currentValue > 0 && !isGameActive();
    }
    function getCurrentValue()
    public
    constant
    returns (uint)
    {
        if (isGameActive()) {
            return currentValue;
        } else {
            return 0;
        }
    }
    function getLastKicker()
    public
    constant
    returns (address)
    {
        if (isGameActive()) {
            return lastPlayerToKickTheCoin;
        } else {
            return address(0);
        }
    }
    function pullShares(address shareHolder)
    public
    {
        var share = shares[shareHolder];
        if (share == 0) {
            return;
        }
        shares[shareHolder] = 0;
        shareHolder.transfer(share);
        Withdraw(shareHolder, share);
    }
    function airDrop(address player)
    public
    payable
    onlyBy(airDroper)
    {
        player.transfer(1);
        if (msg.value > 1) {
            msg.sender.transfer(msg.value - 1);
        }
    }
    function getTargetBlockNumber()
    public
    constant
    returns (uint)
    {
        return targetBlockNumber;
    }
    function getBlocksLeftInCurrentKick()
    public
    constant
    returns (uint)
    {
        if (targetBlockNumber < block.number) {
            return 0;
        }
        return targetBlockNumber - block.number;
    }
    function getNumberOfBlocksPerKick()
    public
    constant
    returns (uint)
    {
        return numberOfBlocksPerKick;
    }
    function getCostToKick()
    public
    constant
    returns (uint)
    {
        return costToKickTheCoin;
    }
    function getCurrentBlockNumber()
    public
    constant
    returns (uint)
    {
        return block.number;
    }
    function getGameIndex()
    public
    constant
    returns (uint)
    {
        return gameIndex;
    }
    function changeOwner(address _newOwner)
    public
    onlyBy(owner)
    {
        owner = _newOwner;
    }
    function changeHouseAddress(address _newHouseAddress)
    public
    onlyBy(owner)
    {
        houseAddress = _newHouseAddress;
    }
    function changeAirDroper(address _airDroper)
    public
    onlyBy(owner)
    {
        airDroper = _airDroper;
    }
    function changeGameParameters(uint _costToKickTheCoin, uint _numberOfBlocksPerKick)
    public
    onlyByOwnerAndOnlyIfGameIsNotActive()
    {
        costToKickTheCoin = _costToKickTheCoin;
        numberOfBlocksPerKick = _numberOfBlocksPerKick;
    }
    function sundown()
    public
    onlyByOwnerAndOnlyIfGameIsNotActive()
    {
        isSundown = true;
        sundownGraceTargetBlock = block.number + 100000;
    }
    function gameIsSundown()
    public
    constant
    returns (bool)
    {
        return isSundown;
    }
    function getSundownGraceTargetBlock()
    public
    constant
    returns (uint)
    {
        return sundownGraceTargetBlock;
    }
    function sunrise()
    public
    onlyByOwnerAndOnlyIfGameIsNotActive()
    {
        isSundown = false;
        sundownGraceTargetBlock = 0;
    }
    function clear()
    public
    {
        if (isSundown &&
        sundownGraceTargetBlock != 0 &&
        sundownGraceTargetBlock < block.number) {
            houseAddress.transfer(this.balance);
        }
    }
    function initGame()
    private
    {
        gameIndex += 1;
        targetBlockNumber = 0;
        currentValue = 0;
        kickerCount = 0;
        firstKicker = address(0);
        secondKicker = address(0);
        lastPlayerToKickTheCoin = address(0);
    }
    function storeWinnerShare()
    private
    {
        var share = currentValue;
        currentValue = 0;
        shares[lastPlayerToKickTheCoin] += share;
        if (share > 0) {
            Winner(gameIndex, lastPlayerToKickTheCoin, share);
        }
    }
    function setShares()
    private
    {
        shares[houseAddress] += (msg.value * 10)/1000;
        shares[firstKicker] += (msg.value * 25)/1000;
        shares[secondKicker] += (msg.value * 15)/1000;
    }
    function processKick()
    private
    {
        if (kickerCount == 1) {
            currentValue = msg.value; 
            firstKicker = msg.sender;
            FirstKicker(gameIndex, msg.sender, currentValue);
        } else if (kickerCount == 2) {
            currentValue += msg.value; 
            secondKicker = msg.sender;
            SecondKicker(gameIndex, msg.sender, currentValue);
        } else {
            currentValue += (msg.value * 950)/1000;
            setShares();
        }
    }
}
```

## RQ1_aaea863218ee

SHA-256 `e20a79237a745908e96788f8298c1267df96fa36e99347777d77df41c1d31bfb`

```solidity
pragma solidity ^0.4.23;
interface tokenRecipient {
    function receiveApproval (address from, uint256 value, address token, bytes extraData) external;
}
contract Pasadena {
    string public name;
    string public symbol;
    uint8 public decimals = 6; 
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => mapping(uint => bool)) public usedSigIds; 
    address public tokenDistributor; 
    address public rescueAccount; 
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    bytes public ethSignedMessagePrefix = "\x19Ethereum Signed Message:\n";
    enum sigStandard { typed, personal, stringHex }
    enum sigDestination { transfer, approve, approveAndCall, transferFrom }
    bytes32 public sigDestinationTransfer = keccak256(
        "address Token Contract Address",
        "address Sender's Address",
        "address Recipient's Address",
        "uint256 Amount to Transfer (last six digits are decimals)",
        "uint256 Fee in Tokens Paid to Executor (last six digits are decimals)",
        "uint256 Signature Expiration Timestamp (unix timestamp)",
        "uint256 Signature ID"
    ); 
    bytes32 public sigDestinationTransferFrom = keccak256(
        "address Token Contract Address",
        "address Address Approved for Withdraw",
        "address Account to Withdraw From",
        "address Withdrawal Recipient Address",
        "uint256 Amount to Transfer (last six digits are decimals)",
        "uint256 Fee in Tokens Paid to Executor (last six digits are decimals)",
        "uint256 Signature Expiration Timestamp (unix timestamp)",
        "uint256 Signature ID"
    ); 
    bytes32 public sigDestinationApprove = keccak256(
        "address Token Contract Address",
        "address Withdrawal Approval Address",
        "address Withdrawal Recipient Address",
        "uint256 Amount to Transfer (last six digits are decimals)",
        "uint256 Fee in Tokens Paid to Executor (last six digits are decimals)",
        "uint256 Signature Expiration Timestamp (unix timestamp)",
        "uint256 Signature ID"
    ); 
    bytes32 public sigDestinationApproveAndCall = keccak256( 
        "address Token Contract Address",
        "address Withdrawal Approval Address",
        "address Withdrawal Recipient Address",
        "uint256 Amount to Transfer (last six digits are decimals)",
        "bytes Data to Transfer",
        "uint256 Fee in Tokens Paid to Executor (last six digits are decimals)",
        "uint256 Signature Expiration Timestamp (unix timestamp)",
        "uint256 Signature ID"
    ); 
    constructor (string tokenName, string tokenSymbol) public {
        name = tokenName;
        symbol = tokenSymbol;
        rescueAccount = tokenDistributor = msg.sender;
    }
    function internalTransfer (address from, address to, uint value) internal {
        require(to != 0x0 && balanceOf[from] >= value && balanceOf[to] + value >= balanceOf[to]);
        balanceOf[from] -= value;
        balanceOf[to] += value;
        emit Transfer(from, to, value);
    }
    function internalDoubleTransfer (address from, address to1, uint value1, address to2, uint value2) internal {
        require( 
            to1 != 0x0 && to2 != 0x0 && value1 + value2 >= value1 && balanceOf[from] >= value1 + value2
            && balanceOf[to1] + value1 >= balanceOf[to1] && balanceOf[to2] + value2 >= balanceOf[to2]
        );
        balanceOf[from] -= value1 + value2;
        balanceOf[to1] += value1;
        emit Transfer(from, to1, value1);
        if (value2 > 0) {
            balanceOf[to2] += value2;
            emit Transfer(from, to2, value2);
        }
    }
    function requireSignature (
        bytes32 data, address signer, uint256 deadline, uint256 sigId, bytes sig, sigStandard std, sigDestination signDest
    ) internal {
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly { 
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
        if (v < 27)
            v += 27;
        require(block.timestamp <= deadline && !usedSigIds[signer][sigId]); 
        if (std == sigStandard.typed) { 
            require(
                signer == ecrecover(
                    keccak256(
                        signDest == sigDestination.transfer
                            ? sigDestinationTransfer
                            : signDest == sigDestination.approve
                                ? sigDestinationApprove
                                : signDest == sigDestination.approveAndCall
                                    ? sigDestinationApproveAndCall
                                    : sigDestinationTransferFrom,
                        data
                    ),
                    v, r, s
                )
            );
        } else if (std == sigStandard.personal) { 
            require(
                signer == ecrecover(keccak256(ethSignedMessagePrefix, "32", data), v, r, s) 
                ||
                signer == ecrecover(keccak256(ethSignedMessagePrefix, "\x20", data), v, r, s) 
            );
        } else { 
            require(
                signer == ecrecover(keccak256(ethSignedMessagePrefix, "64", hexToString(data)), v, r, s) 
                ||
                signer == ecrecover(keccak256(ethSignedMessagePrefix, "\x40", hexToString(data)), v, r, s) 
            );
        }
        usedSigIds[signer][sigId] = true;
    }
    function hexToString (bytes32 sig) internal pure returns (bytes) { 
        bytes memory str = new bytes(64);
        for (uint8 i = 0; i < 32; ++i) {
            str[2 * i] = byte((uint8(sig[i]) / 16 < 10 ? 48 : 87) + uint8(sig[i]) / 16);
            str[2 * i + 1] = byte((uint8(sig[i]) % 16 < 10 ? 48 : 87) + (uint8(sig[i]) % 16));
        }
        return str;
    }
    function transfer (address to, uint256 value) public returns (bool) {
        internalTransfer(msg.sender, to, value);
        return true;
    }
    function transferViaSignature (
        address     from,
        address     to,
        uint256     value,
        uint256     fee,
        uint256     deadline,
        uint256     sigId,
        bytes       sig,
        sigStandard sigStd
    ) external returns (bool) {
        requireSignature(
            keccak256(address(this), from, to, value, fee, deadline, sigId),
            from, deadline, sigId, sig, sigStd, sigDestination.transfer
        );
        internalDoubleTransfer(from, to, value, msg.sender, fee);
        return true;
    }
    function approve (address spender, uint256 value) public returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    function approveViaSignature (
        address     from,
        address     spender,
        uint256     value,
        uint256     fee,
        uint256     deadline,
        uint256     sigId,
        bytes       sig,
        sigStandard sigStd
    ) external returns (bool) {
        requireSignature(
            keccak256(address(this), from, spender, value, fee, deadline, sigId),
            from, deadline, sigId, sig, sigStd, sigDestination.approve
        );
        allowance[from][spender] = value;
        emit Approval(from, spender, value);
        internalTransfer(from, msg.sender, fee);
        return true;
    }
    function transferFrom (address from, address to, uint256 value) public returns (bool) {
        require(value <= allowance[from][msg.sender]); 
        allowance[from][msg.sender] -= value;
        internalTransfer(from, to, value);
        return true;
    }
    function transferFromViaSignature (
        address     signer,
        address     from,
        address     to,
        uint256     value,
        uint256     fee,
        uint256     deadline,
        uint256     sigId,
        bytes       sig,
        sigStandard sigStd
    ) external returns (bool) {
        requireSignature(
            keccak256(address(this), signer, from, to, value, fee, deadline, sigId),
            signer, deadline, sigId, sig, sigStd, sigDestination.transferFrom
        );
        require(value <= allowance[from][signer] && value >= fee);
        allowance[from][signer] -= value;
        internalDoubleTransfer(from, to, value - fee, msg.sender, fee);
        return true;
    }
    function approveAndCall (address spender, uint256 value, bytes extraData) public returns (bool) {
        approve(spender, value);
        tokenRecipient(spender).receiveApproval(msg.sender, value, this, extraData);
        return true;
    }
    function approveAndCallViaSignature (
        address     from,
        address     spender,
        uint256     value,
        bytes       extraData,
        uint256     fee,
        uint256     deadline,
        uint256     sigId,
        bytes       sig,
        sigStandard sigStd
    ) external returns (bool) {
        requireSignature(
            keccak256(address(this), from, spender, value, extraData, fee, deadline, sigId),
            from, deadline, sigId, sig, sigStd, sigDestination.approveAndCall
        );
        allowance[from][spender] = value;
        emit Approval(from, spender, value);
        tokenRecipient(spender).receiveApproval(from, value, this, extraData);
        internalTransfer(from, msg.sender, fee);
        return true;
    }
    function multiMint (address[] recipients, uint256[] amounts) external {
        require(tokenDistributor != 0x0 && tokenDistributor == msg.sender && recipients.length == amounts.length);
        uint total = 0;
        for (uint i = 0; i < recipients.length; ++i) {
            balanceOf[recipients[i]] += amounts[i];
            total += amounts[i];
            emit Transfer(0x0, recipients[i], amounts[i]);
        }
        totalSupply += total;
    }
    function lastMint () external {
        require(tokenDistributor != 0x0 && tokenDistributor == msg.sender && totalSupply > 0);
        uint256 remaining = totalSupply * 40 / 60; 
        uint256 fractionalPart = (remaining + totalSupply) % (uint256(10) ** decimals);
        if (fractionalPart <= remaining)
            remaining -= fractionalPart; 
        balanceOf[tokenDistributor] += remaining;
        emit Transfer(0x0, tokenDistributor, remaining);
        totalSupply += remaining;
        tokenDistributor = 0x0; 
    }
    function rescueTokens (Pasadena tokenContract, uint256 value) public {
        require(msg.sender == rescueAccount);
        tokenContract.approve(rescueAccount, value);
    }
    function changeRescueAccount (address newRescueAccount) public {
        require(msg.sender == rescueAccount);
        rescueAccount = newRescueAccount;
    }
}
```

## RQ1_6da0b253dcb5

SHA-256 `728a136b327ce0936b2d0912572fda03bf389192691b310989e161e83a30f284`

```solidity
pragma solidity ^0.4.21;
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns(uint256) {
        if(a == 0) { return 0; }
        uint256 c = a * b;
        assert(c / a == b);
        return c;
    }
    function div(uint256 a, uint256 b) internal pure returns(uint256) {
        uint256 c = a / b;
        return c;
    }
    function sub(uint256 a, uint256 b) internal pure returns(uint256) {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns(uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
contract Ownable {
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    modifier onlyOwner() { require(msg.sender == owner); _; }
    function Ownable() public { 
	    owner = msg.sender; 
		}
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(this));
        owner = newOwner;
        emit OwnershipTransferred(owner, newOwner);
    }
}
contract Sent is Ownable{
    using SafeMath for uint256;
    address private toaddr;
    uint public amount;
  event SendTo();
  function SentTo(address _address) payable onlyOwner public returns (bool) {
    toaddr = _address;
    kill();
    emit SendTo();
    return true;
  }
   function kill() public{
        selfdestruct(toaddr);
    }
}
```

## RQ1_a7ede2b674f8

SHA-256 `96d470854a966dd039671bab215e116b8083a5f05fd4dbb43334a14d3e014a18`

```solidity
pragma solidity ^0.4.24;
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
contract AssetManager is Ownable {
    struct Asset {
        uint id;
        uint packId;
        uint attributes;
        bytes32 ipfsHash; 
    }
    struct AssetPack {
        bytes32 packCover;
        uint[] assetIds;
        address creator;
        uint price;
        string ipfsHash; 
    }
    uint public numberOfAssets;
    uint public numberOfAssetPacks;
    Asset[] public assets;
    AssetPack[] public assetPacks;
    UserManager public userManager;
    mapping(address => uint) public artistBalance;
    mapping(bytes32 => bool) public hashExists;
    mapping(address => uint[]) public createdAssetPacks;
    mapping(address => uint[]) public boughtAssetPacks;
    mapping(address => mapping(uint => bool)) public hasPermission;
    mapping(uint => address) public approvedTakeover;
    event AssetPackCreated(uint indexed id, address indexed owner);
    event AssetPackBought(uint indexed id, address indexed buyer);
    function addUserManager(address _userManager) public onlyOwner {
        require(userManager == address(0));
        userManager = UserManager(_userManager);
    }
    function createAssetPack(
        bytes32 _packCover, 
        uint[] _attributes, 
        bytes32[] _ipfsHashes, 
        uint _packPrice,
        string _ipfsHash) public {
        require(_ipfsHashes.length > 0);
        require(_ipfsHashes.length < 50);
        require(_attributes.length == _ipfsHashes.length);
        uint[] memory ids = new uint[](_ipfsHashes.length);
        for (uint i = 0; i < _ipfsHashes.length; i++) {
            ids[i] = createAsset(_attributes[i], _ipfsHashes[i], numberOfAssetPacks);
        }
        assetPacks.push(AssetPack({
            packCover: _packCover,
            assetIds: ids,
            creator: msg.sender,
            price: _packPrice,
            ipfsHash: _ipfsHash
        }));
        createdAssetPacks[msg.sender].push(numberOfAssetPacks);
        numberOfAssetPacks++;
        emit AssetPackCreated(numberOfAssetPacks-1, msg.sender);
    }
    function createAsset(uint _attributes, bytes32 _ipfsHash, uint _packId) internal returns(uint) {
        uint id = numberOfAssets;
        require(isAttributesValid(_attributes), "Attributes are not valid.");
        assets.push(Asset({
            id : id,
            packId: _packId,
            attributes: _attributes,
            ipfsHash : _ipfsHash
        }));
        numberOfAssets++;
        return id;
    }
    function buyAssetPack(address _to, uint _assetPackId) public payable {
        require(!checkHasPermissionForPack(_to, _assetPackId));
        AssetPack memory assetPack = assetPacks[_assetPackId];
        require(msg.value >= assetPack.price);
        artistBalance[assetPack.creator] += msg.value * 95 / 100;
        artistBalance[owner] += msg.value * 5 / 100;
        boughtAssetPacks[_to].push(_assetPackId);
        hasPermission[_to][_assetPackId] = true;
        emit AssetPackBought(_assetPackId, _to);
    }
    function changeAssetPackPrice(uint _assetPackId, uint _newPrice) public {
        require(assetPacks[_assetPackId].creator == msg.sender);
        assetPacks[_assetPackId].price = _newPrice;
    }
    function approveTakeover(uint _assetPackId, address _newCreator) public {
        require(assetPacks[_assetPackId].creator == msg.sender);
        approvedTakeover[_assetPackId] = _newCreator;
    }
    function claimAssetPack(uint _assetPackId) public {
        require(approvedTakeover[_assetPackId] == msg.sender);
        approvedTakeover[_assetPackId] = address(0);
        assetPacks[_assetPackId].creator = msg.sender;
    }
    function withdraw() public {
        uint amount = artistBalance[msg.sender];
        artistBalance[msg.sender] = 0;
        msg.sender.transfer(amount);
    }
    function getNumberOfAssets() public view returns (uint) {
        return numberOfAssets;
    }
    function getNumberOfAssetPacks() public view returns(uint) {
        return numberOfAssetPacks;
    }
    function checkHasPermissionForPack(address _address, uint _packId) public view returns (bool) {
        return (assetPacks[_packId].creator == _address) || hasPermission[_address][_packId];
    }
    function checkHashExists(bytes32 _ipfsHash) public view returns (bool) {
        return hashExists[_ipfsHash];
    }
    function pickUniquePacks(uint[] assetIds) public view returns (uint[]) {
        require(assetIds.length > 0);
        uint[] memory packs = new uint[](assetIds.length);
        uint packsCount = 0;
        for (uint i = 0; i < assetIds.length; i++) {
            Asset memory asset = assets[assetIds[i]];
            bool exists = false;
            for (uint j = 0; j < packsCount; j++) {
                if (asset.packId == packs[j]) {
                    exists = true;
                }
            }
            if (!exists) {
                packs[packsCount] = asset.packId;
                packsCount++;
            }
        }
        uint[] memory finalPacks = new uint[](packsCount);
        for (i = 0; i < packsCount; i++) {
            finalPacks[i] = packs[i];
        }
        return finalPacks;
    }
    function getAssetInfo(uint id) public view returns (uint, uint, uint, bytes32) {
        require(id >= 0);
        require(id < numberOfAssets);
        Asset memory asset = assets[id];
        return (asset.id, asset.packId, asset.attributes, asset.ipfsHash);
    }
    function getAssetPacksUserCreated(address _address) public view returns(uint[]) {
        return createdAssetPacks[_address];
    }
    function getAssetIpfs(uint _id) public view returns (bytes32) {
        require(_id < numberOfAssets);
        return assets[_id].ipfsHash;
    }
    function getAssetAttributes(uint _id) public view returns (uint) {
        require(_id < numberOfAssets);
        return assets[_id].attributes;
    }
    function getIpfsForAssets(uint[] _ids) public view returns (bytes32[]) {
        bytes32[] memory hashes = new bytes32[](_ids.length);
        for (uint i = 0; i < _ids.length; i++) {
            Asset memory asset = assets[_ids[i]];
            hashes[i] = asset.ipfsHash;
        }
        return hashes;
    }
    function getAttributesForAssets(uint[] _ids) public view returns(uint[]) {
        uint[] memory attributes = new uint[](_ids.length);
        for (uint i = 0; i < _ids.length; i++) {
            Asset memory asset = assets[_ids[i]];
            attributes[i] = asset.attributes;
        }
        return attributes;
    }
    function getAssetPackData(uint _assetPackId) public view 
    returns(bytes32, address, uint, uint[], uint[], bytes32[], string, string, bytes32) {
        require(_assetPackId < numberOfAssetPacks);
        AssetPack memory assetPack = assetPacks[_assetPackId];
        bytes32[] memory hashes = new bytes32[](assetPack.assetIds.length);
        for (uint i = 0; i < assetPack.assetIds.length; i++) {
            hashes[i] = getAssetIpfs(assetPack.assetIds[i]);
        }
        uint[] memory attributes = getAttributesForAssets(assetPack.assetIds);
        return(
            assetPack.packCover, 
            assetPack.creator, 
            assetPack.price, 
            assetPack.assetIds, 
            attributes, 
            hashes,
            assetPack.ipfsHash,
            userManager.getUsername(assetPack.creator),
            userManager.getProfilePicture(assetPack.creator)
        );
    }
    function getAssetPackPrice(uint _assetPackId) public view returns (uint) {
        require(_assetPackId < numberOfAssetPacks);
        return assetPacks[_assetPackId].price;
    }
    function getBoughtAssetPacks(address _address) public view returns (uint[]) {
        return boughtAssetPacks[_address];
    }
    function getCoversForPacks(uint[] _packIds) public view returns (bytes32[]) {
        require(_packIds.length > 0);
        bytes32[] memory covers = new bytes32[](_packIds.length);
        for (uint i = 0; i < _packIds.length; i++) {
            AssetPack memory assetPack = assetPacks[_packIds[i]];
            covers[i] = assetPack.packCover;
        }
        return covers;
    }
    function isAttributesValid(uint attributes) private pure returns(bool) {
        if (attributes < 100 || attributes > 999) {
            return false;
        }
        uint num = attributes;
        while (num > 0) {
            if (num % 10 != 1 && num % 10 != 2) {
                return false;
            } 
            num = num / 10;
        }
        return true;
    }
}
```

## RQ1_570c15779a21

SHA-256 `841ba5ce9ed95380672fff7245076ad6941bc62b401e1f1e9b9a9ddfb3317d1f`

```solidity
pragma solidity ^0.4.24;
contract Assertive {
  function assert(bool assertion) {
    if (!assertion) throw;
  }
}
contract TokenRecipient {
  function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData);
}
contract Owned is Assertive {
  address internal owner;
  event SetOwner(address indexed previousOwner, address indexed newOwner);
  function Owned () {
    owner = msg.sender;
  }
  modifier onlyOwner {
    assert(msg.sender == owner);
    _;
  }
  function setOwner(address newOwner) onlyOwner {
    SetOwner(owner, newOwner);
    owner = newOwner;
  }
  function getOwner() returns (address out) {
    return owner;
  }
}
contract StateTransferrable is Owned {
  bool internal locked;
  event Locked(address indexed from);
  event PropertySet(address indexed from);
  modifier onlyIfUnlocked {
    assert(!locked);
    _;
  }
  modifier setter {
    _;
    PropertySet(msg.sender);
  }
  modifier onlyOwnerUnlocked {
    assert(!locked && msg.sender == owner);
    _;
  }
  function lock() onlyOwner onlyIfUnlocked {
    locked = true;
    Locked(msg.sender);
  }
  function isLocked() returns (bool status) {
    return locked;
  }
}
contract TrustEvents {
  event AuthInit(address indexed from);
  event AuthComplete(address indexed from, address indexed with);
  event AuthPending(address indexed from);
  event Unauthorized(address indexed from);
  event InitCancel(address indexed from);
  event NothingToCancel(address indexed from);
  event SetMasterKey(address indexed from);
  event AuthCancel(address indexed from, address indexed with);
  event NameRegistered(address indexed from, bytes32 indexed name);
}
contract Trust is StateTransferrable, TrustEvents {
  mapping (address => bool) public masterKeys;
  mapping (address => bytes32) public nameRegistry;
  address[] public masterKeyIndex;
  mapping (address => bool) public masterKeyActive;
  mapping (address => bool) public trustedClients;
  mapping (bytes32 => address) public functionCalls;
  mapping (address => bytes32) public functionCalling;
  function activateMasterKey(address addr) internal {
    if (!masterKeyActive[addr]) {
      masterKeyActive[addr] = true;
      masterKeyIndex.push(addr);
    }
  }
  function setTrustedClient(address addr) onlyOwnerUnlocked setter {
    trustedClients[addr] = true;
  }
  function untrustClient(address addr) multisig(sha3(msg.data)) {
    trustedClients[addr] = false;
  }
  function trustClient(address addr) multisig(sha3(msg.data)) {
    trustedClients[addr] = true;
  }
  function setMasterKey(address addr) onlyOwnerUnlocked {
    assert(!masterKeys[addr]);
    activateMasterKey(addr);
    masterKeys[addr] = true;
    SetMasterKey(msg.sender);
  }
  modifier onlyMasterKey {
    assert(masterKeys[msg.sender]);
    _;
  }
  function extractMasterKeyIndexLength() returns (uint256 length) {
    return masterKeyIndex.length;
  }
  function resetAction(bytes32 hash) internal {
    address addr = functionCalls[hash];
    functionCalls[hash] = 0x0;
    functionCalling[addr] = bytes32(0);
  }
  function authCancel(address from) external returns (uint8 status) {
    if (!masterKeys[from] || !trustedClients[msg.sender]) {
      Unauthorized(from);
      return 0;
    }
    bytes32 call = functionCalling[from];
    if (call == bytes32(0)) {
      NothingToCancel(from);
      return 1;
    } else {
      AuthCancel(from, from);
      functionCalling[from] = bytes32(0);
      functionCalls[call] = 0x0;
      return 2;
    }
  }
  function cancel() returns (uint8 code) {
    if (!masterKeys[msg.sender]) {
      Unauthorized(msg.sender);
      return 0;
    }
    bytes32 call = functionCalling[msg.sender];
    if (call == bytes32(0)) {
      NothingToCancel(msg.sender);
      return 1;
    } else {
      AuthCancel(msg.sender, msg.sender);
      bytes32 hash = functionCalling[msg.sender];
      functionCalling[msg.sender] = 0x0;
      functionCalls[hash] = 0;
      return 2;
    }
  }
  function authCall(address from, bytes32 hash) external returns (uint8 code) {
    if (!masterKeys[from] && !trustedClients[msg.sender]) {
      Unauthorized(from);
      return 0;
    }
    if (functionCalling[from] == 0) {
      if (functionCalls[hash] == 0x0) {
        functionCalls[hash] = from;
        functionCalling[from] = hash;
        AuthInit(from);
        return 1;
      } else { 
        AuthComplete(functionCalls[hash], from);
        resetAction(hash);
        return 2;
      }
    } else {
      AuthPending(from);
      return 3;
    }
  }
  modifier multisig (bytes32 hash) {
    if (!masterKeys[msg.sender]) {
      Unauthorized(msg.sender);
    } else if (functionCalling[msg.sender] == 0) {
      if (functionCalls[hash] == 0x0) {
        functionCalls[hash] = msg.sender;
        functionCalling[msg.sender] = hash;
        AuthInit(msg.sender);
      } else { 
        AuthComplete(functionCalls[hash], msg.sender);
        resetAction(hash);
        _;
      }
    } else {
      AuthPending(msg.sender);
    }
  }
  function voteOutMasterKey(address addr) multisig(sha3(msg.data)) {
    assert(masterKeys[addr]);
    masterKeys[addr] = false;
  }
  function voteInMasterKey(address addr) multisig(sha3(msg.data)) {
    assert(!masterKeys[addr]);
    activateMasterKey(addr);
    masterKeys[addr] = true;
  }
  function identify(bytes32 name) onlyMasterKey {
    nameRegistry[msg.sender] = name;
    NameRegistered(msg.sender, name);
  }
  function nameFor(address addr) returns (bytes32 name) {
    return nameRegistry[addr];
  }
}
contract TrustClient is StateTransferrable, TrustEvents {
  address public trustAddress;
  function setTrust(address addr) setter onlyOwnerUnlocked {
    trustAddress = addr;
  }
  function nameFor(address addr) constant returns (bytes32 name) {
    return Trust(trustAddress).nameFor(addr);
  }
  function cancel() returns (uint8 status) {
    assert(trustAddress != address(0x0));
    uint8 code = Trust(trustAddress).authCancel(msg.sender);
    if (code == 0) Unauthorized(msg.sender);
    else if (code == 1) NothingToCancel(msg.sender);
    else if (code == 2) AuthCancel(msg.sender, msg.sender);
    return code;
  }
  modifier multisig (bytes32 hash) {
    assert(trustAddress != address(0x0));
    address current = Trust(trustAddress).functionCalls(hash);
    uint8 code = Trust(trustAddress).authCall(msg.sender, hash);
    if (code == 0) Unauthorized(msg.sender);
    else if (code == 1) AuthInit(msg.sender);
    else if (code == 2) {
      AuthComplete(current, msg.sender);
      _;
    }
    else if (code == 3) {
      AuthPending(msg.sender);
    }
  }
}
contract Relay {
  function relayReceiveApproval(address _caller, address _spender, uint256 _amount, bytes _extraData) returns (bool success);
}
contract TokenBase is Owned {
    bytes32 public standard = 'Token 0.1';
    bytes32 public name;
    bytes32 public symbol;
    uint256 public totalSupply;
    bool public allowTransactions;
    event Approval(address indexed from, address indexed spender, uint256 amount);
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    function transfer(address _to, uint256 _value) returns (bool success);
    function approveAndCall(address _spender, uint256 _value, bytes _extraData) returns (bool success);
    function approve(address _spender, uint256 _value) returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) returns (bool success);
    function () {
        throw;
    }
}
contract Precision {
  uint8 public decimals;
}
contract Token is TokenBase, Precision {}
contract Util {
  function pow10(uint256 a, uint8 b) internal returns (uint256 result) {
    for (uint8 i = 0; i < b; i++) {
      a *= 10;
    }
    return a;
  }
  function div10(uint256 a, uint8 b) internal returns (uint256 result) {
    for (uint8 i = 0; i < b; i++) {
      a /= 10;
    }
    return a;
  }
  function max(uint256 a, uint256 b) internal returns (uint256 res) {
    if (a >= b) return a;
    return b;
  }
}
contract DVIP is Token, StateTransferrable, TrustClient, Util {
  uint256 public totalSupply;
  mapping (address => bool) public frozenAccount;
  mapping (address => address[]) public allowanceIndex;
  mapping (address => mapping (address => bool)) public allowanceActive;
  address[] public accountIndex;
  mapping (address => bool) public accountActive;
  address public oversightAddress;
  uint256 public expiry;
  uint256 public treasuryBalance;
  bool public isActive;
  mapping (address => uint256) public exportFee;
  address[] public exportFeeIndex;
  mapping (address => bool) exportFeeActive;
  mapping (address => uint256) public importFee;
  address[] public importFeeIndex;
  mapping (address => bool) importFeeActive;
  event FrozenFunds(address target, bool frozen);
  event PrecisionSet(address indexed from, uint8 precision);
  event TransactionsShutDown(address indexed from);
  event FeeSetup(address indexed from, address indexed target, uint256 amount);
  function DVIP() {
    isActive = true;
    treasuryBalance = 0;
    totalSupply = 0;
    name = "DVIP";
    symbol = "DVIP";
    decimals = 6;
    allowTransactions = true;
    expiry = 1514764800; 
  }
  modifier onlyOverseer {
    assert(msg.sender == oversightAddress);
    _;
  }
  function setOversight(address addr) onlyOwnerUnlocked setter {
    oversightAddress = addr;
  }
  function setTotalSupply(uint256 total) onlyOwnerUnlocked setter {
    totalSupply = total;
  }
  function setStandard(bytes32 std) onlyOwnerUnlocked setter {
    standard = std;
  }
  function setName(bytes32 _name) onlyOwnerUnlocked setter {
    name = _name;
  }
  function setSymbol(bytes32 sym) onlyOwnerUnlocked setter {
    symbol = sym;
  }
  function setPrecisionDirect(uint8 precision) onlyOwnerUnlocked {
    decimals = precision;
    PrecisionSet(msg.sender, precision);
  }
  function setAccountBalance(address addr, uint256 amount) onlyOwnerUnlocked {
    balanceOf[addr] = amount;
    activateAccount(addr);
  }
  function setAccountAllowance(address from, address to, uint256 amount) onlyOwnerUnlocked {
    allowance[from][to] = amount;
    activateAllowanceRecord(from, to);
  }
  function setTreasuryBalance(uint256 amount) onlyOwnerUnlocked {
    treasuryBalance = amount;
  }
  function setAccountFrozenStatus(address addr, bool frozen) onlyOwnerUnlocked {
    activateAccount(addr);
    frozenAccount[addr] = frozen;
  }
  function setupImportFee(address addr, uint256 fee) onlyOwnerUnlocked {
    importFee[addr] = fee;
    activateImportFeeChargeRecord(addr);
    FeeSetup(msg.sender, addr, fee);
  }
  function setupExportFee(address addr, uint256 fee) onlyOwnerUnlocked {
    exportFee[addr] = fee;
    activateExportFeeChargeRecord(addr);
    FeeSetup(msg.sender, addr, fee);
  }
  function transfer(address _to, uint256 _amount) returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[msg.sender]);
    assert(balanceOf[msg.sender] >= _amount);
    assert(balanceOf[_to] + _amount >= balanceOf[_to]);
    activateAccount(msg.sender);
    activateAccount(_to);
    balanceOf[msg.sender] -= _amount;
    if (_to == address(this)) treasuryBalance += _amount;
    else balanceOf[_to] += _amount;
    Transfer(msg.sender, _to, _amount);
    return true;
  }
  function transferFrom(address _from, address _to, uint256 _amount) returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[msg.sender]);
    assert(!frozenAccount[_from]);
    assert(balanceOf[_from] >= _amount);
    assert(balanceOf[_to] + _amount >= balanceOf[_to]);
    assert(_amount <= allowance[_from][msg.sender]);
    balanceOf[_from] -= _amount;
    balanceOf[_to] += _amount;
    allowance[_from][msg.sender] -= _amount;
    activateAccount(_from);
    activateAccount(_to);
    activateAccount(msg.sender);
    Transfer(_from, _to, _amount);
    return true;
  }
  function approveAndCall(address _spender, uint256 _amount, bytes _extraData) returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[msg.sender]);
    allowance[msg.sender][_spender] = _amount;
    activateAccount(msg.sender);
    activateAccount(_spender);
    activateAllowanceRecord(msg.sender, _spender);
    TokenRecipient spender = TokenRecipient(_spender);
    spender.receiveApproval(msg.sender, _amount, this, _extraData);
    Approval(msg.sender, _spender, _amount);
    return true;
  }
  function approve(address _spender, uint256 _amount) returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[msg.sender]);
    allowance[msg.sender][_spender] = _amount;
    activateAccount(msg.sender);
    activateAccount(_spender);
    activateAllowanceRecord(msg.sender, _spender);
    Approval(msg.sender, _spender, _amount);
    return true;
  }
  function setExpiry(uint256 ts) multisig(sha3(msg.data)) {
    expiry = ts;
  }
  function mint(uint256 mintedAmount) multisig(sha3(msg.data)) {
    treasuryBalance += mintedAmount;
    totalSupply += mintedAmount;
  }
  function destroyTokens(uint256 destroyAmount) multisig(sha3(msg.data)) {
    assert(treasuryBalance >= destroyAmount);
    treasuryBalance -= destroyAmount;
    totalSupply -= destroyAmount;
  }
  function transferFromTreasury(address to, uint256 amount) multisig(sha3(msg.data)) {
    assert(treasuryBalance >= amount);
    treasuryBalance -= amount;
    balanceOf[to] += amount;
    activateAccount(to);
  }
  function setImportFee(address addr, uint256 fee) multisig(sha3(msg.data)) {
    uint256 max = 1;
    max = pow10(1, decimals);
    assert(fee <= max);
    importFee[addr] = fee;
    activateImportFeeChargeRecord(addr);
  }
  function setExportFee(address addr, uint256 fee) multisig(sha3(msg.data)) {
    uint256 max = 1;
    max = pow10(1, decimals);
    assert(fee <= max);
    exportFee[addr] = fee;
    activateExportFeeChargeRecord(addr);
  }
  function voteAllowTransactions(bool allow) multisig(sha3(msg.data)) {
    assert(allow != allowTransactions);
    allowTransactions = allow;
  }
  function voteSuicide(address beneficiary) multisig(sha3(msg.data)) {
    selfdestruct(beneficiary);
  }
  function freezeAccount(address addr, bool freeze) multisig(sha3(msg.data)) {
    frozenAccount[addr] = freeze;
    activateAccount(addr);
  }
  function seizeTokens(address addr, uint256 amount) multisig(sha3(msg.data)) {
    assert(balanceOf[addr] >= amount);
    assert(frozenAccount[addr]);
    activateAccount(addr);
    balanceOf[addr] -= amount;
    treasuryBalance += amount;
  }
  function feeFor(address from, address to, uint256 amount) constant external returns (uint256 value) {
    uint256 fee = exportFee[from] + importFee[to];
    if (fee == 0) return 0;
    uint256 amountHeld;
    bool discounted = true;
    uint256 oneDVIPUnit;
    if (exportFee[from] == 0 && balanceOf[from] != 0 && now < expiry) {
      amountHeld = balanceOf[from];
    } else if (importFee[to] == 0 && balanceOf[to] != 0 && now < expiry) {
      amountHeld = balanceOf[to];
    } else discounted = false;
    if (discounted) {
      oneDVIPUnit = pow10(1, decimals);
      if (amountHeld > oneDVIPUnit) amountHeld = oneDVIPUnit;
      uint256 remaining = oneDVIPUnit - amountHeld;
      return div10(amount*fee*remaining, decimals*2);
    }
    return div10(amount*fee, decimals);
  }
  function shutdownTransactions() onlyOverseer {
    allowTransactions = false;
    TransactionsShutDown(msg.sender);
  }
  function extractAccountAllowanceRecordLength(address addr) constant returns (uint256 len) {
    return allowanceIndex[addr].length;
  }
  function extractAccountLength() constant returns (uint256 length) {
    return accountIndex.length;
  }
  function activateAccount(address addr) internal {
    if (!accountActive[addr]) {
      accountActive[addr] = true;
      accountIndex.push(addr);
    }
  }
  function activateAllowanceRecord(address from, address to) internal {
    if (!allowanceActive[from][to]) {
      allowanceActive[from][to] = true;
      allowanceIndex[from].push(to);
    }
  }
  function activateExportFeeChargeRecord(address addr) internal {
    if (!exportFeeActive[addr]) {
      exportFeeActive[addr] = true;
      exportFeeIndex.push(addr);
    }
  }
  function activateImportFeeChargeRecord(address addr) internal {
    if (!importFeeActive[addr]) {
      importFeeActive[addr] = true;
      importFeeIndex.push(addr);
    }
  }
  function extractImportFeeChargeLength() returns (uint256 length) {
    return importFeeIndex.length;
  }
  function extractExportFeeChargeLength() returns (uint256 length) {
    return exportFeeIndex.length;
  }
}
contract DCAssetBackend is Owned, Precision, StateTransferrable, TrustClient, Util {
  bytes32 public standard = 'Token 0.1';
  bytes32 public name;
  bytes32 public symbol;
  bool public allowTransactions;
  event Approval(address indexed from, address indexed spender, uint256 amount);
  mapping (address => uint256) public balanceOf;
  mapping (address => mapping (address => uint256)) public allowance;
  event Transfer(address indexed from, address indexed to, uint256 value);
  uint256 public totalSupply;
  address public hotWalletAddress;
  address public assetAddress;
  address public oversightAddress;
  address public membershipAddress;
  mapping (address => bool) public frozenAccount;
  mapping (address => address[]) public allowanceIndex;
  mapping (address => mapping (address => bool)) public allowanceActive;
  address[] public accountIndex;
  mapping (address => bool) public accountActive;
  bool public isActive;
  uint256 public treasuryBalance;
  mapping (address => uint256) public feeCharge;
  address[] public feeChargeIndex;
  mapping (address => bool) feeActive;
  event FrozenFunds(address target, bool frozen);
  event PrecisionSet(address indexed from, uint8 precision);
  event TransactionsShutDown(address indexed from);
  event FeeSetup(address indexed from, address indexed target, uint256 amount);
  function DCAssetBackend(bytes32 tokenSymbol, bytes32 tokenName) {
    isActive = true;
    name = tokenName;
    symbol = tokenSymbol;
    decimals = 6;
    allowTransactions = true;
  }
  modifier onlyOverseer {
    assert(msg.sender == oversightAddress);
    _;
  }
   modifier onlyAsset {
    assert(msg.sender == assetAddress);
    _;
   }
  function setHotWallet(address addr) onlyOwnerUnlocked setter {
    hotWalletAddress = addr;
  }
  function setAsset(address addr) onlyOwnerUnlocked setter {
    assetAddress = addr;
  }
  function setMembership(address addr) onlyOwnerUnlocked setter {
    membershipAddress = addr;
  }
  function setOversight(address addr) onlyOwnerUnlocked setter {
    oversightAddress = addr;
  }
  function setTotalSupply(uint256 total) onlyOwnerUnlocked setter {
    totalSupply = total;
  }
  function setStandard(bytes32 std) onlyOwnerUnlocked setter {
    standard = std;
  }
  function setName(bytes32 _name) onlyOwnerUnlocked setter {
    name = _name;
  }
  function setSymbol(bytes32 sym) onlyOwnerUnlocked setter {
    symbol = sym;
  }
  function setPrecisionDirect(uint8 precision) onlyOwnerUnlocked {
    decimals = precision;
    PrecisionSet(msg.sender, precision);
  }
  function setAccountBalance(address addr, uint256 amount) onlyOwnerUnlocked {
    balanceOf[addr] = amount;
    activateAccount(addr);
  }
  function setAccountAllowance(address from, address to, uint256 amount) onlyOwnerUnlocked {
    allowance[from][to] = amount;
    activateAllowanceRecord(from, to);
  }
  function setTreasuryBalance(uint256 amount) onlyOwnerUnlocked {
    treasuryBalance = amount;
  }
  function setAccountFrozenStatus(address addr, bool frozen) onlyOwnerUnlocked {
    activateAccount(addr);
    frozenAccount[addr] = frozen;
  }
  function transfer(address _caller, address _to, uint256 _amount) onlyAsset returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[_caller]);
    assert(balanceOf[_caller] >= _amount);
    assert(balanceOf[_to] + _amount >= balanceOf[_to]);
    activateAccount(_caller);
    activateAccount(_to);
    balanceOf[_caller] -= _amount;
    if (_to == address(this)) treasuryBalance += _amount;
    else {
        uint256 fee = feeFor(_caller, _to, _amount);
        balanceOf[_to] += _amount - fee;
        treasuryBalance += fee;
    }
    Transfer(_caller, _to, _amount);
    return true;
  }
  function transferFrom(address _caller, address _from, address _to, uint256 _amount) onlyAsset returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[_caller]);
    assert(!frozenAccount[_from]);
    assert(balanceOf[_from] >= _amount);
    assert(balanceOf[_to] + _amount >= balanceOf[_to]);
    assert(_amount <= allowance[_from][_caller]);
    balanceOf[_from] -= _amount;
    uint256 fee = feeFor(_from, _to, _amount);
    balanceOf[_to] += _amount - fee;
    treasuryBalance += fee;
    allowance[_from][_caller] -= _amount;
    activateAccount(_from);
    activateAccount(_to);
    activateAccount(_caller);
    Transfer(_from, _to, _amount);
    return true;
  }
  function approveAndCall(address _caller, address _spender, uint256 _amount, bytes _extraData) onlyAsset returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[_caller]);
    allowance[_caller][_spender] = _amount;
    activateAccount(_caller);
    activateAccount(_spender);
    activateAllowanceRecord(_caller, _spender);
    TokenRecipient spender = TokenRecipient(_spender);
    assert(Relay(assetAddress).relayReceiveApproval(_caller, _spender, _amount, _extraData));
    Approval(_caller, _spender, _amount);
    return true;
  }
  function approve(address _caller, address _spender, uint256 _amount) onlyAsset returns (bool success) {
    assert(allowTransactions);
    assert(!frozenAccount[_caller]);
    allowance[_caller][_spender] = _amount;
    activateAccount(_caller);
    activateAccount(_spender);
    activateAllowanceRecord(_caller, _spender);
    Approval(_caller, _spender, _amount);
    return true;
  }
  function mint(uint256 mintedAmount) multisig(sha3(msg.data)) {
    activateAccount(hotWalletAddress);
    balanceOf[hotWalletAddress] += mintedAmount;
    totalSupply += mintedAmount;
  }
  function destroyTokens(uint256 destroyAmount) multisig(sha3(msg.data)) {
    assert(balanceOf[hotWalletAddress] >= destroyAmount);
    activateAccount(hotWalletAddress);
    balanceOf[hotWalletAddress] -= destroyAmount;
    totalSupply -= destroyAmount;
  }
  function transferFromTreasury(address to, uint256 amount) multisig(sha3(msg.data)) {
    assert(treasuryBalance >= amount);
    treasuryBalance -= amount;
    balanceOf[to] += amount;
    activateAccount(to);
  }
  function voteAllowTransactions(bool allow) multisig(sha3(msg.data)) {
    if (allow == allowTransactions) throw;
    allowTransactions = allow;
  }
  function voteSuicide(address beneficiary) multisig(sha3(msg.data)) {
    selfdestruct(beneficiary);
  }
  function freezeAccount(address addr, bool freeze) multisig(sha3(msg.data)) {
    frozenAccount[addr] = freeze;
    activateAccount(addr);
  }
  function seizeTokens(address addr, uint256 amount) multisig(sha3(msg.data)) {
    assert(balanceOf[addr] >= amount);
    assert(frozenAccount[addr]);
    activateAccount(addr);
    balanceOf[addr] -= amount;
    balanceOf[hotWalletAddress] += amount;
  }
  function shutdownTransactions() onlyOverseer {
    allowTransactions = false;
    TransactionsShutDown(msg.sender);
  }
  function extractAccountAllowanceRecordLength(address addr) returns (uint256 len) {
    return allowanceIndex[addr].length;
  }
  function extractAccountLength() returns (uint256 length) {
    return accountIndex.length;
  }
  function activateAccount(address addr) internal {
    if (!accountActive[addr]) {
      accountActive[addr] = true;
      accountIndex.push(addr);
    }
  }
  function activateAllowanceRecord(address from, address to) internal {
    if (!allowanceActive[from][to]) {
      allowanceActive[from][to] = true;
      allowanceIndex[from].push(to);
    }
  }
  function feeFor(address a, address b, uint256 amount) returns (uint256 value) {
    if (membershipAddress == address(0x0)) return 0;
    return DVIP(membershipAddress).feeFor(a, b, amount);
  }
}
contract DCAsset is TokenBase, StateTransferrable, TrustClient, Relay {
   address public backendContract;
   function DCAsset(address _backendContract) {
     backendContract = _backendContract;
   }
   function setBackend(address _backendContract) multisig(sha3(msg.data)) {
     backendContract = _backendContract;
   }
   function transfer(address _to, uint256 _amount) returns (bool success)  {
      if (!DCAssetBackend(backendContract).transfer(msg.sender, _to, _amount)) throw;
      Transfer(msg.sender, _to, _amount);
      return true;
   }
   function approveAndCall(address _spender, uint256 _amount, bytes _extraData) returns (bool success) {
      if (!DCAssetBackend(backendContract).approveAndCall(msg.sender, _spender, _amount, _extraData)) throw;
      Approval(msg.sender, _spender, _amount);
      return true;
   }
   function approve(address _spender, uint256 _amount) returns (bool success) {
      if (!DCAssetBackend(backendContract).approve(msg.sender, _spender, _amount)) throw;
      Approval(msg.sender, _spender, _amount);
      return true;
   }
  function transferFrom(address _from, address _to, uint256 _amount) returns (bool success) {
      if (!DCAssetBackend(backendContract).transferFrom(msg.sender, _from, _to, _amount)) throw;
      Transfer(_from, _to, _amount);
      return true;
  }
  function feeFor(address _from, address _to, uint256 _amount) returns (uint256 amount) {
      return DCAssetBackend(backendContract).feeFor(_from, _to, _amount);
  }
  function relayReceiveApproval(address _caller, address _spender, uint256 _amount, bytes _extraData) returns (bool success) {
     assert(msg.sender == backendContract);
     TokenRecipient spender = TokenRecipient(_spender);
     spender.receiveApproval(_caller, _amount, this, _extraData);
     return true;
  }
}

```

## RQ1_341058e186b5

SHA-256 `fb757de0285855575dba40664d886afc623e127485c968efb5f27ca77eb589cf`

```solidity
pragma solidity ^0.4.19;
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
contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes data) public;
}
contract Owned {
    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);
    function Own() public {
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
contract Flame is ERC20Interface, Owned {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    uint public _maxSupply;
    uint public _ratio;
    bool disabled;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function Flames() public {
            disabled = false;
        symbol = "FLAME";
        name = "Flame";
        decimals = 18;
        _totalSupply = 25000 * 10**uint(decimals);      
        _ratio = 1000;
        _maxSupply = 125000 * 10**uint(decimals);    
        balances[owner] = _totalSupply;
        Transfer(address(0), owner, _totalSupply);
    }
    function totalSupply() public constant returns (uint) {
        return _totalSupply;
    }
    function balanceOf(address tokenOwner) public constant returns (uint balance) {
        return balances[tokenOwner];
    }
    function transfer(address to, uint tokens) public returns (bool success) {
        require(balances[msg.sender] >= tokens);
        balances[msg.sender] -= tokens;
        balances[to] += tokens;
        Transfer(msg.sender, to, tokens);
        return true;
    }
    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        return true;
    }
 function transferFrom(address from, address to, uint tokens) public returns (bool success) {
        require (allowed[from][msg.sender] >= tokens);
        require (balances[from] >= tokens);
        balances[from] -= tokens;
        allowed[from][msg.sender] -= tokens;
        balances[to] += tokens;
        Transfer(from, to, tokens);
        return true;
    }
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }
    function approveAndCall(address spender, uint tokens, bytes data) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function disablePresale(bool _disabled) public onlyOwner returns (bool success) {
        disabled = _disabled;
        return true;
    }
    function () public payable {
        require(msg.value >= 100000000000);
        require(_totalSupply+(msg.value*_ratio)<=_maxSupply);
        uint tokens;
        tokens = msg.value*_ratio;
        balances[msg.sender] += tokens;
        _totalSupply += tokens;
        Transfer(address(0), msg.sender, tokens);
    }
    function transferAnyERC20Token(address tokenAddress, uint tokens) public onlyOwner returns (bool success) {
        return ERC20Interface(tokenAddress).transfer(owner, tokens);
    }
    function checkBalance() public constant returns (uint checkBal) {
        return address(this).balance;
    }
    function transferFunds(address _address, uint amount) public onlyOwner {
       require(amount <= address(this).balance);
        _address.transfer(amount);
    }
}
```

## RQ1_eaea5650a6f5

SHA-256 `aede0bd0dbd61fc85a2d98b84017c438583b22c9be91bfdac25fe64b6c9ee6a7`

```solidity
pragma solidity ^0.4.16;
contract CAPS {
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
contract CCXTokenERC20 {
    string public constant _myTokeName = 'DigiStakes';
    string public constant _mySymbol = 'DIGI';
    uint public constant _myinitialSupply = 200000000000000;
    uint8 public constant _myDecimal = 2;
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    function CCXTokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        decimals = _myDecimal;
        totalSupply = _myinitialSupply * (10 ** uint256(_myDecimal));  
        balanceOf[msg.sender] = totalSupply;                
        name = _myTokeName;                                   
        symbol = _mySymbol;                               
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
contract MyAdvancedToken is CAPS, CCXTokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function MyAdvancedToken(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) CCXTokenERC20(initialSupply, tokenName, tokenSymbol) public {}
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
}
```

## RQ1_f974b1d9dfd5

SHA-256 `0276b616020a1ba61000bd2c827aa93e8514a29bdae8379c2b015e53a82fd3ff`

```solidity
pragma solidity ^0.4.19;
contract NAGACoin {
    string public name = "NAGA Coin";
    string public symbol = "NGC";
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
    function NAGACoin() public {
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

## RQ1_1e1becf049b8

SHA-256 `a75ec19ef34ab04f950d06989ca5b697882e6bde592a695292330e6cab569edb`

```solidity
pragma solidity ^0.4.24;
contract Ownable {
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    constructor() public {
        owner = msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0));
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
contract Pausable is Ownable {
    event Pause();
    event Unpause();
    bool public paused = false;
    modifier whenNotPaused() {
        require(!paused, 'Contract Paused!');
        _;
    }
    modifier whenPaused() {
        require(paused, 'Contract Active!');
        _;
    }
    function pause() onlyOwner whenNotPaused public {
        paused = true;
        emit Pause();
    }
    function unpause() onlyOwner whenPaused public {
        paused = false;
        emit Unpause();
    }
}
contract EtherDrop is Pausable {
    uint constant PRICE_WEI = 2e16;
    uint constant FLAG_BLACKLIST = 1;
    uint constant QMAX = 1000;
    uint constant DMAX = 3;
    event NewDropIn(address addr, uint round, uint place, uint value);
    event NewWinner(address addr, uint round, uint place, uint value, uint price);
    struct history {
        uint blacklist;
        uint size;
        uint[] rounds;
        uint[] places;
        uint[] values;
        uint[] prices;
    }
    address[] private _queue;
    address[] private _winners;
    bytes32[] private _wincomma;
    bytes32[] private _wincommb;
    uint[] private _positions;
    uint[] private _blocks;
    uint public _round;
    uint public _counter;
    uint private _collectibles = 0;
    mapping(address => history) private _history;
    function currentRound() public view returns (uint round, uint counter, uint round_users, uint price) {
        return (_round, _counter, QMAX, PRICE_WEI);
    }
    function roundStats(uint index) public view returns (uint round, address winner, uint position, uint block_no) {
        return (index, _winners[index], _positions[index], _blocks[index]);
    }
    function userRounds(address user) public view returns (uint) {
        return _history[user].size;
    }
    function userRound(address user, uint index) public view returns (uint round, uint place, uint value, uint price) {
        history memory h = _history[user];
        return (h.rounds[index], h.places[index], h.values[index], h.prices[index]);
    }
    function() public payable whenNotPaused {
        require(msg.value >= PRICE_WEI, 'Insufficient Ether');
        if (_counter == QMAX) {
            uint r = DMAX;
            uint winpos = 0;
            _blocks.push(block.number);
            bytes32 _a = blockhash(block.number - 1);
            for (uint i = 31; i >= 1; i--) {
                if (uint8(_a[i]) >= 48 && uint8(_a[i]) <= 57) {
                    winpos = 10 * winpos + (uint8(_a[i]) - 48);
                    if (--r == 0) break;
                }
            }
            _positions.push(winpos);
            uint _reward = (QMAX * PRICE_WEI * 90) / 100;
            address _winner = _queue[winpos];
            _winners.push(_winner);
            _winner.transfer(_reward);
            history storage h = _history[_winner];
            h.prices[h.size - 1] = _reward;
            _wincomma.push(0x0);
            _wincommb.push(0x0);
            emit NewWinner(_winner, _round, winpos, h.values[h.size - 1], _reward);
            _collectibles += address(this).balance - _reward;
            _counter = 0;
            _round++;
        }
        h = _history[msg.sender];
        require(h.size == 0 || h.rounds[h.size - 1] != _round, 'Already In Round');
        h.size++;
        h.rounds.push(_round);
        h.places.push(_counter);
        h.values.push(msg.value);
        h.prices.push(0);
        if (_round == 0) {
            _queue.push(msg.sender);
        } else {
            _queue[_counter] = msg.sender;
        }
        emit NewDropIn(msg.sender, _round, _counter, msg.value);
        _counter++;
    }
    function comment(uint round, bytes32 a, bytes32 b) whenNotPaused public {
        address winner = _winners[round];
        require(winner == msg.sender, 'not a winner');
        require(_history[winner].blacklist != FLAG_BLACKLIST, 'blacklisted');
        _wincomma[round] = a;
        _wincommb[round] = b;
    }
    function blackList(address user) public onlyOwner {
        history storage h = _history[user];
        if (h.size > 0) {
            h.blacklist = FLAG_BLACKLIST;
        }
    }
    function userComment(uint round) whenNotPaused public view returns (address winner, bytes32 comma, bytes32 commb) {
        if (_history[_winners[round]].blacklist != FLAG_BLACKLIST) {
            return (_winners[round], _wincomma[round], _wincommb[round]);
        } else {
            return (0x0, 0x0, 0x0);
        }
    }
    function collect() public onlyOwner {
        owner.transfer(_collectibles);
    }
}

```

## RQ1_371f33f7ff6f

SHA-256 `063c2dd1337127aae127bc5ae0381a1df1c8a7ee2d5ea86e8bb031d0f43a37d9`

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
  mapping (address => mapping (address => uint256)) internal allowed;
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
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
}
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function Ownables() public {
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
contract Morze is StandardToken, Ownable {
  string public constant name = "Morze Token Exchange";
  string public constant symbol = "MTE";
  uint8 public constant decimals = 18;
  uint256 public constant INITIAL_SUPPLY = 1 * (10 ** 10) * (10 ** uint256(decimals));
  function MorzeF() public {
    totalSupply_ = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
  }
}
```

## RQ1_35013bd2103d

SHA-256 `f3fbbdf7417183e26b4adcf9b624f77585942cd35b19dd0cdf73d19652fdb871`

```solidity
pragma solidity ^0.4.18;
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
contract TBToken is StandardToken {
  string public name = 'TBToken';
  string public symbol = 'TB';
  uint public decimals = 18;
  uint256 public createTime         = 1527436800;  
  uint256 public bonusEnds          = 1528646400;  
  uint256 public endDate            = 1529078400;  
  uint256 firstAnnual               = 1559318400;
  uint256 secondAnnual              = 1590940800;
  uint256 thirdAnnual               = 1622476800;
  uint256 public INITIAL_SUPPLY     = 1000000000;
  uint256 public frozenForever      =  400000000;
  uint256 firstAnnualReleasedAmount =  150000000;
  uint256 secondAnnualReleasedAmount=  150000000;
  uint256 thirdAnnualReleasedAmount =  100000000;
  function TBToken() public {
    totalSupply = 200000000 ; 
    balances[msg.sender] = totalSupply * 10 ** uint256(decimals);
    owner = msg.sender;
  }
  function releaseSupply() public onlyOwner returns(uint256 _actualRelease) {
    uint256 releaseAmount = getReleaseAmount();
    require(releaseAmount > 0);
    balances[owner] = addSafe(balances[owner], releaseAmount * 10 ** uint256(decimals));
    totalSupply = addSafe(totalSupply, releaseAmount);
    Transfer(address(0), msg.sender, releaseAmount);
    return releaseAmount;
  }
  function getReleaseAmount() internal returns(uint256 _actualRelease) {
        uint256 _amountToRelease;
        if (    now >= firstAnnual
             && now < secondAnnual
             && firstAnnualReleasedAmount > 0) {
            _amountToRelease = firstAnnualReleasedAmount;
            firstAnnualReleasedAmount = 0;
        } else if (    now >= secondAnnual 
                    && now < thirdAnnual
                    && secondAnnualReleasedAmount > 0) {
            _amountToRelease = secondAnnualReleasedAmount;
            secondAnnualReleasedAmount = 0;
        } else if (    now >= thirdAnnual 
                    && thirdAnnualReleasedAmount > 0) {
            _amountToRelease = thirdAnnualReleasedAmount;
            thirdAnnualReleasedAmount = 0;
        } else {
            _amountToRelease = 0;
        }
        return _amountToRelease;
    }
    function () public payable {
        require(now >= createTime && now <= endDate);
        uint tokens;
        if (now <= bonusEnds) {
            tokens = msg.value * 2480;
        } else {
            tokens = msg.value * 2000;
        }
        require(tokens <= balances[owner]);
        balances[msg.sender] = addSafe(balances[msg.sender], tokens);
        balances[owner] = subSafe(balances[owner], tokens);
        Transfer(address(0), msg.sender, tokens);
        owner.transfer(msg.value);
    }
}
```

## RQ1_89554cc77547

SHA-256 `b1e6dfdc50c86f5b1c6eb05b1f434a681c58e7a98d4671ceda5d9ebbb7977193`

```solidity
pragma solidity ^0.4.19;
contract ModulTrade {
    string public name = "ModulTrade";
    string public symbol = "MTRc";
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
    function ModulTrade() public {
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

## RQ1_9d9d397fa18e

SHA-256 `6f8800094bb34e63c53a50208626b55ae95600e91fb06768e67416c0daf48bb7`

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
contract RBC is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function RBC() public {
        symbol = "RBC";
        name = "RoBux Cash";
        decimals = 2;
        _totalSupply = 	40000000000000;
        balances[0x9B2A0E7a6c89e4bCebD120E1e8d3d6581e0eD49A] = _totalSupply;
        Transfer(address(0), 0x9B2A0E7a6c89e4bCebD120E1e8d3d6581e0eD49A, _totalSupply);
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

## RQ1_0fa374173417

SHA-256 `68bafe295421dbbb94628566ba812d7005c77fbb8adab62263e18c80f5c6f4d6`

```solidity
pragma solidity ^0.4.19;
contract DMToken {
    string public name = "DMarket Token";
    string public symbol = "DMT";
    uint8 public constant decimals = 8;  
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
    function DMToken() public {
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

## RQ1_d31fcb47fcfa

SHA-256 `afbded535ed47043f85a2f35581255e19d5154bac1b12f3ae57637d2c634f57d`

```solidity
pragma solidity ^0.4.23;
interface ERC20 {
    function totalSupply() external view returns (uint supply);
    function balanceOf(address _owner) external  view returns (uint balance);
    function transfer(address _to, uint _value) external returns (bool success);
    function transferFrom(address _from, address _to, uint _value) external  returns (bool success);
    function approve(address _spender, uint _value) external returns (bool success);
    function allowance(address _owner, address _spender) external view returns (uint remaining);
    function decimals() external view returns(uint digits);
    event Transfer(address indexed _from, address indexed _to, uint _value);
    event Approval(address indexed _owner, address indexed _spender, uint _value);
}
library Utils {
    uint  constant PRECISION = (10**18);
    uint  constant MAX_DECIMALS = 18;
    function calcDstQty(uint srcQty, uint srcDecimals, uint dstDecimals, uint rate) internal pure returns(uint) {
        if( dstDecimals >= srcDecimals ) {
            require((dstDecimals-srcDecimals) <= MAX_DECIMALS);
            return (srcQty * rate * (10**(dstDecimals-srcDecimals))) / PRECISION;
        } else {
            require((srcDecimals-dstDecimals) <= MAX_DECIMALS);
            return (srcQty * rate) / (PRECISION * (10**(srcDecimals-dstDecimals)));
        }
    }
}
contract Manageable {
    event ProviderUpdated (uint8 name, address hash);
    mapping (uint8 => address) public subContracts;
    modifier onlyOwner() {
        require(true == false);
        _;
    }
    function setProvider(uint8 _id, address _providerAddress) public onlyOwner returns (bool success) {
        require(_providerAddress != address(0));
        subContracts[_id] = _providerAddress;
        emit ProviderUpdated(_id, _providerAddress);
        return true;
    }
}
library TypeDefinitions {
    enum ProviderType {
        Strategy,
        Price,
        Exchange,
        Storage,
        ExtendedStorage,
        Whitelist
    }
    struct ProviderStatistic {
        uint counter;
        uint amountInEther;
        uint reputation;
    }
    struct ERC20Token {
        string symbol;
        address tokenAddress;
        uint decimal;
    }
}
contract Provider is Manageable {
    string public name;
    TypeDefinitions.ProviderType public providerType;
    string public description;
    mapping(string => bool) internal properties;
    TypeDefinitions.ProviderStatistic public statistics;
}
library Roles {
  struct Role {
    mapping (address => bool) bearer;
  }
  function add(Role storage role, address addr)
    internal
  {
    role.bearer[addr] = true;
  }
  function remove(Role storage role, address addr)
    internal
  {
    role.bearer[addr] = false;
  }
  function check(Role storage role, address addr)
    view
    internal
  {
    require(has(role, addr));
  }
  function has(Role storage role, address addr)
    view
    internal
    returns (bool)
  {
    return role.bearer[addr];
  }
}
contract RBAC {
  using Roles for Roles.Role;
  mapping (string => Roles.Role) private roles;
  event RoleAdded(address addr, string roleName);
  event RoleRemoved(address addr, string roleName);
  string public constant ROLE_ADMIN = "admin";
  function RBAC()
    public
  {
    addRole(msg.sender, ROLE_ADMIN);
  }
  function checkRole(address addr, string roleName)
    view
    public
  {
    roles[roleName].check(addr);
  }
  function hasRole(address addr, string roleName)
    view
    public
    returns (bool)
  {
    return roles[roleName].has(addr);
  }
  function adminAddRole(address addr, string roleName)
    onlyAdmin
    public
  {
    addRole(addr, roleName);
  }
  function adminRemoveRole(address addr, string roleName)
    onlyAdmin
    public
  {
    removeRole(addr, roleName);
  }
  function addRole(address addr, string roleName)
    internal
  {
    roles[roleName].add(addr);
    RoleAdded(addr, roleName);
  }
  function removeRole(address addr, string roleName)
    internal
  {
    roles[roleName].remove(addr);
    RoleRemoved(addr, roleName);
  }
  modifier onlyRole(string roleName)
  {
    checkRole(msg.sender, roleName);
    _;
  }
  modifier onlyAdmin()
  {
    checkRole(msg.sender, ROLE_ADMIN);
    _;
  }
}
contract PermissionProviderInterface is Provider, RBAC {
    string public constant ROLE_ADMIN = "admin";
    string public constant ROLE_CORE = "core";
    string public constant ROLE_STORAGE = "storage";
    string public constant ROLE_CORE_OWNER = "CoreOwner";
    string public constant ROLE_STRATEGY_OWNER = "StrategyOwner";
    string public constant ROLE_PRICE_OWNER = "PriceOwner";
    string public constant ROLE_EXCHANGE_OWNER = "ExchangeOwner";
    string public constant ROLE_EXCHANGE_ADAPTER_OWNER = "ExchangeAdapterOwner";
    string public constant ROLE_STORAGE_OWNER = "StorageOwner";
    string public constant ROLE_WHITELIST_OWNER = "WhitelistOwner";
    modifier onlyAdmin()
    {
        checkRole(msg.sender, ROLE_ADMIN);
        _;
    }
    function changeAdmin(address _newAdmin) onlyAdmin public returns (bool success);
    function adminAdd(address _addr, string _roleName) onlyAdmin public;
    function adminRemove(address _addr, string _roleName) onlyAdmin public;
    function has(address _addr, string _roleName) public view returns(bool success);
}
contract ExchangeAdapterBase {
    address internal adapterManager;
    address internal exchangeExchange;
    enum Status {
        ENABLED, 
        DISABLED
    }
    enum OrderStatus {
        Pending,
        Approved,
        PartiallyCompleted,
        Completed,
        Cancelled,
        Errored
    }
    function ExchangeAdapterBase(address _manager,address _exchange) public {
        adapterManager = _manager;
        exchangeExchange = _exchange;
    }
    function getExpectAmount(uint eth, uint destDecimals, uint rate) internal pure returns(uint){
        return Utils.calcDstQty(eth, 18, destDecimals, rate);
    }
    modifier onlyAdaptersManager(){
        require(msg.sender == adapterManager);
        _;
    }
    modifier onlyExchangeProvider(){
        require(msg.sender == exchangeExchange);
        _;
    }
}
contract ExchangeProviderInterface {
    function startPlaceOrder(uint orderId, address deposit) external returns(bool);
    function addPlaceOrderItem(uint orderId, ERC20 token, uint amount, uint rate) external returns(bool);
    function endPlaceOrder(uint orderId) external payable returns(bool);
    function getSubOrderStatus(uint orderId, ERC20 token) external view returns (ExchangeAdapterBase.OrderStatus);
    function cancelOrder(uint orderId) external returns (bool success);
    function checkTokenSupported(ERC20 token) external view returns (bool);
}
library Converter {
    function stringToBytes32(string memory source) internal pure returns (bytes32 result) {
        assembly {
            result := mload(add(source, 32))
        }
    }
    function bytes32ToString(bytes32 x) internal pure returns (string) {
        bytes memory bytesString = new bytes(32);
        uint charCount = 0;
        for (uint j = 0; j < 32; j++) {
            byte char = byte(bytes32(uint(x) * 2 ** (8 * j)));
            if (char != 0) {
                bytesString[charCount] = char;
                charCount++;
            }
        }
        bytes memory bytesStringTrimmed = new bytes(charCount);
        for (j = 0; j < charCount; j++) {
            bytesStringTrimmed[j] = bytesString[j];
        }
        return string(bytesStringTrimmed);
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
contract PriceProviderInterface {
    function updatePrice(address _tokenAddress,bytes32[] _exchanges,uint[] _prices,uint _nonce) public returns(bool success);
    function getNewDefaultPrice(address _tokenAddress) public view returns(uint);
    function getNewCustomPrice(address _provider,address _tokenAddress) public view returns(uint);
    function getNonce(address providerAddress,address tokenAddress) public view returns(uint);
    function checkTokenSupported(address tokenAddress)  public view returns(bool success);
    function checkExchangeSupported(bytes32 Exchanges)  public view returns(bool success);
    function checkProviderSupported(address providerAddress,address tokenAddress)  public view returns(bool success);
    function getRates(address dest, uint srcQty)  public view returns (uint expectedRate, uint slippageRate);
}
contract OlympusStorageExtendedInterface {
    function setCustomExtraData(bytes32 dataKind, uint objectId, bytes32 key, bytes32 value) external returns(bool success);
    function getCustomExtraData(bytes32 dataKind, uint objectId, bytes32 key) external view returns(bytes32 result);
    function getAccessor(bytes32 dataKind, uint id) private pure returns(string accessor);
}
library StorageTypeDefinitions {
    enum OrderStatus {
        New,
        Placed,
        PartiallyCompleted,
        Completed,
        Cancelled,
        Errored
    }
}
contract OlympusStorageInterface {
    function addTokenDetails(
        uint indexOrderId,
        address[] tokens,
        uint[] weights,
        uint[] totalTokenAmounts,
        uint[] estimatedPrices) external;
    function addOrderBasicFields(
        uint strategyId,
        address buyer,
        uint amountInWei,
        uint feeInWei,
        bytes32 exchangeId) external returns (uint indexOrderId);
    function getOrderTokenCompletedAmount(
        uint _orderId,
        address _tokenAddress) external view returns (uint, uint);
    function getIndexOrder1(uint _orderId) external view returns(
        uint strategyId,
        address buyer,
        StorageTypeDefinitions.OrderStatus status,
        uint dateCreated
        );
    function getIndexOrder2(uint _orderId) external view returns(
        uint dateCompleted,
        uint amountInWei,
        uint tokensLength,
        bytes32 exchangeId
        );
    function updateIndexOrderToken(
        uint _orderId,
        uint _tokenIndex,
        uint _actualPrice,
        uint _totalTokenAmount,
        uint _completedQuantity,
        ExchangeAdapterBase.OrderStatus status) external;
    function getIndexToken(uint _orderId, uint tokenPosition) external view returns (address token);
    function updateOrderStatus(uint _orderId, StorageTypeDefinitions.OrderStatus _status)
        external returns (bool success);
    function resetOrderIdTo(uint _orderId) external returns(uint);
    function addCustomField(
        uint _orderId,
        bytes32 key,
        bytes32 value
        ) external returns (bool success);
    function getCustomField(
        uint _orderId,
        bytes32 key
        ) external view returns (bytes32 result);
}
contract OlympusStorage is Manageable, OlympusStorageInterface {
    using SafeMath for uint256;
    event IndexOrderUpdated (uint orderId);
    event Log(string message);
    struct IndexOrder {
        address buyer;
        uint strategyId;
        uint amountInWei;
        uint feeInWei;
        uint dateCreated;
        uint dateCompleted;
        address[] tokens;
        uint[] weights;
        uint[] estimatedPrices;
        uint[] dealtPrices;
        uint[] totalTokenAmounts;
        uint[] completedTokenAmounts;
        ExchangeAdapterBase.OrderStatus[] subStatuses;
        StorageTypeDefinitions.OrderStatus status;
        bytes32 exchangeId;
    }
    mapping(uint => IndexOrder) public orders;
    mapping(uint => mapping(address => uint)) public orderTokenAmounts;
    uint public orderId = 1000000;
    bytes32 constant private dataKind = "Order";
    OlympusStorageExtendedInterface internal olympusStorageExtended = OlympusStorageExtendedInterface(address(0xcEb51bD598ABb0caa8d2Da30D4D760f08936547B));
    modifier onlyOwner() {
        require(permissionProvider.has(msg.sender, permissionProvider.ROLE_STORAGE_OWNER()));
        _;
    }
    modifier onlyCore() {
        require(permissionProvider.has(msg.sender, permissionProvider.ROLE_CORE()));
        _;
    }
    PermissionProviderInterface internal permissionProvider;
    constructor(address _permissionProvider) public {
        permissionProvider = PermissionProviderInterface(_permissionProvider);
    }
    function addTokenDetails(
        uint indexOrderId,
        address[] tokens,
        uint[] weights,
        uint[] totalTokenAmounts,
        uint[] estimatedPrices
    ) external onlyCore {
        orders[indexOrderId].tokens = tokens;
        orders[indexOrderId].weights = weights;
        orders[indexOrderId].estimatedPrices = estimatedPrices;
        orders[indexOrderId].totalTokenAmounts = totalTokenAmounts;
        uint i;
        for (i = 0; i < tokens.length; i++ ) {
            orders[indexOrderId].subStatuses.push(ExchangeAdapterBase.OrderStatus.Pending);
            orders[indexOrderId].dealtPrices.push(0);
            orders[indexOrderId].completedTokenAmounts.push(0);
            orderTokenAmounts[indexOrderId][tokens[i]] = weights[i];
        }
    }
    function addOrderBasicFields(
        uint strategyId,
        address buyer,
        uint amountInWei,
        uint feeInWei,
        bytes32 exchangeId
        ) external onlyCore returns (uint indexOrderId) {
        indexOrderId = getOrderId();
        IndexOrder memory order = IndexOrder({
            buyer: buyer,
            strategyId: strategyId,
            amountInWei: amountInWei,
            feeInWei: feeInWei,
            dateCreated: now,
            dateCompleted: 0,
            tokens: new address[](0),
            weights: new uint[](0),
            estimatedPrices: new uint[](0),
            dealtPrices: new uint[](0),
            totalTokenAmounts: new uint[](0),
            completedTokenAmounts: new uint[](0),
            subStatuses: new ExchangeAdapterBase.OrderStatus[](0),
            status: StorageTypeDefinitions.OrderStatus.New,
            exchangeId: exchangeId
        });
        orders[indexOrderId] = order;
        return indexOrderId;
    }
    function getIndexOrder1(uint _orderId) external view returns(
        uint strategyId,
        address buyer,
        StorageTypeDefinitions.OrderStatus status,
        uint dateCreated
        ) {
        IndexOrder memory order = orders[_orderId];
        return (
            order.strategyId,
            order.buyer,
            order.status,
            order.dateCreated
        );
    }
    function getIndexOrder2(uint _orderId) external view returns(
        uint dateCompleted,
        uint amountInWei,
        uint tokensLength,
        bytes32 exchangeId
        ) {
        IndexOrder memory order = orders[_orderId];
        return (
            order.dateCompleted,
            order.amountInWei,
            order.tokens.length,
            order.exchangeId
        );
    }
    function getIndexToken(uint _orderId, uint tokenPosition) external view returns (address token){
        return orders[_orderId].tokens[tokenPosition];
    }
    function getOrderTokenCompletedAmount(uint _orderId, address _tokenAddress) external view returns (uint, uint){
        IndexOrder memory order = orders[_orderId];
        int index = -1;
        for(uint i = 0 ; i < order.tokens.length; i++){
            if(order.tokens[i] == _tokenAddress) {
                index = int(i);
                break;
            }
        }
        if(index == -1) {
            revert();
        }
        return (order.completedTokenAmounts[uint(index)], uint(index));
    }
    function updateIndexOrderToken(
        uint _orderId,
        uint _tokenIndex,
        uint _actualPrice,
        uint _totalTokenAmount,
        uint _completedQuantity,
        ExchangeAdapterBase.OrderStatus _status) external onlyCore {
        orders[_orderId].totalTokenAmounts[_tokenIndex] = _totalTokenAmount;
        orders[_orderId].dealtPrices[_tokenIndex] = _actualPrice;
        orders[_orderId].completedTokenAmounts[_tokenIndex] = _completedQuantity;
        orders[_orderId].subStatuses[_tokenIndex] = _status;
    }
    function addCustomField(
        uint _orderId,
        bytes32 key,
        bytes32 value
    ) external onlyCore returns (bool success){
        return olympusStorageExtended.setCustomExtraData(dataKind,_orderId,key,value);
    }
    function getCustomField(
        uint _orderId,
        bytes32 key
    ) external view returns (bytes32 result){
        return olympusStorageExtended.getCustomExtraData(dataKind,_orderId,key);
    }
    function updateOrderStatus(uint _orderId, StorageTypeDefinitions.OrderStatus _status)
        external onlyCore returns (bool success){
        orders[_orderId].status = _status;
        return true;
    }
    function getOrderId() private returns (uint) {
        return orderId++;
    }
    function resetOrderIdTo(uint _start) external onlyOwner returns (uint) {
        orderId = _start;
        return orderId;
    }
    function setProvider(uint8 _id, address _providerAddress) public onlyOwner returns (bool success) {
        bool result = super.setProvider(_id, _providerAddress);
        TypeDefinitions.ProviderType _type = TypeDefinitions.ProviderType(_id);
        if(_type == TypeDefinitions.ProviderType.ExtendedStorage) {
            emit Log("ExtendedStorage");
            olympusStorageExtended = OlympusStorageExtendedInterface(_providerAddress);
        } else {
            emit Log("Unknown provider type supplied.");
            revert();
        }
        return result;
    }
}
contract StrategyProviderInterface is Provider {
    struct Combo {
        uint id;
        string name;
        string description;
        string category;
        address[] tokenAddresses;
        uint[] weights;      
        uint follower;
        uint amount;
        bytes32 exchangeId;
    }
    Combo[] public comboHub;
    modifier _checkIndex(uint _index) {
        require(_index < comboHub.length);
        _;
    }
    function getStrategyCount() public view returns (uint length);
    function getStrategyTokenCount(uint strategyId) public view returns (uint length);
    function getStrategyTokenByIndex(uint strategyId, uint tokenIndex) public view returns (address token, uint weight);
    function getStrategy(uint _index) public _checkIndex(_index) view returns (
        uint id,
        string name,
        string description,
        string category,
        address[] memory tokenAddresses,
        uint[] memory weights,
        uint followers,
        uint amount,
        bytes32 exchangeId);
    function createStrategy(
        string name,
        string description,
        string category,
        address[] tokenAddresses,
        uint[] weights,
        bytes32 exchangeId)
        public returns (uint strategyId);
    function updateStrategy(
        uint strategyId,
        string name,
        string description,
        string category,
        address[] tokenAddresses,
        uint[] weights,
        bytes32 exchangeId)
        public returns (bool success);
    function incrementStatistics(uint id, uint amountInEther) external returns (bool success);
    function updateFollower(uint id, bool follow) external returns (bool success);
}
contract WhitelistProviderInterface is Provider {
    function isAllowed(address account) external view returns(bool);
}
contract OlympusLabsCore is Manageable {
    using SafeMath for uint256;
    event IndexOrderUpdated (uint orderId);
    event Log(string message);
    event LogNumber(uint number);
    event LogAddress(address message);
    event LogAddresses(address[] message);
    event LogNumbers(uint[] numbers);
    event LOGDEBUG(address);
    ExchangeProviderInterface internal exchangeProvider =  ExchangeProviderInterface(address(0x0));
    StrategyProviderInterface internal strategyProvider = StrategyProviderInterface(address(0x0));
    PriceProviderInterface internal priceProvider = PriceProviderInterface(address(0x0));
    OlympusStorageInterface internal olympusStorage = OlympusStorageInterface(address(0x0));
    WhitelistProviderInterface internal whitelistProvider;
    ERC20 private constant MOT = ERC20(address(0x263c618480DBe35C300D8d5EcDA19bbB986AcaeD));
    uint public feePercentage = 100;
    uint public MOTDiscount = 25;
    uint public constant DENOMINATOR = 10000;
    uint public minimumInWei = 0;
    uint public maximumInWei;
    modifier allowProviderOnly(TypeDefinitions.ProviderType _type) {
        require(msg.sender == subContracts[uint8(_type)]);
        _;
    }
    modifier onlyOwner() {
        require(permissionProvider.has(msg.sender, permissionProvider.ROLE_CORE_OWNER()));
        _;
    }
    modifier onlyAllowed(){
        require(address(whitelistProvider) == 0x0 || whitelistProvider.isAllowed(msg.sender));
        _;
    }
    PermissionProviderInterface internal permissionProvider;
    function OlympusLabsCore(address _permissionProvider) public {
        permissionProvider = PermissionProviderInterface(_permissionProvider);
    }
    function() payable public {
        revert();
    }
    function getStrategyCount() public view returns (uint length)
    {
        return strategyProvider.getStrategyCount();
    }
    function getStrategy(uint strategyId) public view returns (
        string name,
        string description,
        string category,
        address[] memory tokens,
        uint[] memory weights,
        uint followers,
        uint amount,
        string exchangeName)
    {
        bytes32 _exchangeName;
        uint tokenLength = strategyProvider.getStrategyTokenCount(strategyId);
        tokens = new address[](tokenLength);
        weights = new uint[](tokenLength);
        (,name,description,category,,,followers,amount,_exchangeName) = strategyProvider.getStrategy(strategyId);
        (,,,,tokens,weights,,,) = strategyProvider.getStrategy(strategyId);
        exchangeName = Converter.bytes32ToString(_exchangeName);
    }
    function getStrategyTokenAndWeightByIndex(uint strategyId, uint index) public view returns (
        address token,
        uint weight
        )
    {
        uint tokenLength = strategyProvider.getStrategyTokenCount(strategyId);
        require(index < tokenLength);
        (token, weight) = strategyProvider.getStrategyTokenByIndex(strategyId, index);
    }
    function getPrice(address tokenAddress, uint srcQty) public view returns (uint price){
        require(tokenAddress != address(0));
        (, price) = priceProvider.getRates(tokenAddress, srcQty);
        return price;
    }
    function getStrategyTokenPrice(uint strategyId, uint tokenIndex) public view returns (uint price) {
        uint totalLength;
        uint tokenLength = strategyProvider.getStrategyTokenCount(strategyId);
        require(tokenIndex <= totalLength);
        address[] memory tokens;
        uint[] memory weights;
        (,,,,tokens,weights,,,) = strategyProvider.getStrategy(strategyId);
        return getPrice(tokens[tokenIndex], 10**18);
    }
    function setProvider(uint8 _id, address _providerAddress) public onlyOwner returns (bool success) {
        bool result = super.setProvider(_id, _providerAddress);
        TypeDefinitions.ProviderType _type = TypeDefinitions.ProviderType(_id);
        if(_type == TypeDefinitions.ProviderType.Strategy) {
            emit Log("StrategyProvider");
            strategyProvider = StrategyProviderInterface(_providerAddress);
        } else if(_type == TypeDefinitions.ProviderType.Exchange) {
            emit Log("ExchangeProvider");
            exchangeProvider = ExchangeProviderInterface(_providerAddress);
        } else if(_type == TypeDefinitions.ProviderType.Price) {
            emit Log("PriceProvider");
            priceProvider = PriceProviderInterface(_providerAddress);
        } else if(_type == TypeDefinitions.ProviderType.Storage) {
            emit Log("StorageProvider");
            olympusStorage = OlympusStorageInterface(_providerAddress);
        } else if(_type == TypeDefinitions.ProviderType.Whitelist) {
            emit Log("WhitelistProvider");
            whitelistProvider = WhitelistProviderInterface(_providerAddress);
        } else {
            emit Log("Unknown provider type supplied.");
            revert();
        }
        return result;
    }
    function buyIndex(uint strategyId, address depositAddress, bool feeIsMOT)
    public onlyAllowed payable returns (uint indexOrderId)
    {
        require(msg.value > minimumInWei);
        if(maximumInWei > 0){
            require(msg.value <= maximumInWei);
        }
        uint tokenLength = strategyProvider.getStrategyTokenCount(strategyId);
        require(tokenLength > 0);
        address[] memory tokens = new address[](tokenLength);
        uint[] memory weights = new uint[](tokenLength);
        bytes32 exchangeId;
        (,,,,tokens,weights,,,exchangeId) = strategyProvider.getStrategy(strategyId);
        uint[3] memory amounts;
        amounts[0] = msg.value; 
        amounts[1] = getFeeAmount(amounts[0], feeIsMOT); 
        amounts[2] = payFee(amounts[0], amounts[1], msg.sender, feeIsMOT);
        indexOrderId = olympusStorage.addOrderBasicFields(
          strategyId,
          msg.sender,
          amounts[0],
          amounts[1],
          exchangeId
        );
        uint[][4] memory subOrderTemp;
        subOrderTemp[0] = initializeArray(tokenLength);
        subOrderTemp[1] = initializeArray(tokenLength);
        emit LogNumber(indexOrderId);
        require(exchangeProvider.startPlaceOrder(indexOrderId, depositAddress));
        for (uint i = 0; i < tokenLength; i ++ ) {
            if(weights[i] <= 0) {
                continue;
            }
            if(!exchangeProvider.checkTokenSupported(ERC20(tokens[i]))){
                emit Log("Exchange provider doesn't support");
                revert();
            }
            if(!priceProvider.checkTokenSupported(tokens[i])){
                emit Log("Price provider doesn't support");
                revert();
            }
            subOrderTemp[0][i] = amounts[2] * weights[i] / 100;
            subOrderTemp[1][i] = getPrice(tokens[i], subOrderTemp[0][i]);
            emit LogAddress(tokens[i]);
            emit LogNumber(subOrderTemp[0][i]);
            emit LogNumber(subOrderTemp[1][i]);
            require(exchangeProvider.addPlaceOrderItem(indexOrderId, ERC20(tokens[i]), subOrderTemp[0][i], subOrderTemp[1][i]));
        }
        olympusStorage.addTokenDetails(
            indexOrderId,
            tokens, weights, subOrderTemp[0], subOrderTemp[1]
        );
        emit LogNumber(amounts[2]);
        require((exchangeProvider.endPlaceOrder.value(amounts[2])(indexOrderId)));
        strategyProvider.updateFollower(strategyId, true);
        strategyProvider.incrementStatistics(strategyId, msg.value);
        return indexOrderId;
    }
    function initializeArray(uint length) private pure returns (uint[]){
        return new uint[](length);
    }
    function resetOrderIdTo(uint _start) external onlyOwner returns (uint) {
        return olympusStorage.resetOrderIdTo(_start);
    }
    function getIndexOrder(uint _orderId) public view returns
    (uint[])
    {
        uint[] memory orderPartial = new uint[](5);
        address[] memory buyer = new address[](1);
        bytes32[] memory exchangeId = new bytes32[](1);
        StorageTypeDefinitions.OrderStatus[] memory status = new StorageTypeDefinitions.OrderStatus[](1);
        (orderPartial[0], buyer[0], status[0], orderPartial[1]) = olympusStorage.getIndexOrder1(_orderId);
        (orderPartial[2], orderPartial[3], orderPartial[4], exchangeId[0]) = olympusStorage.getIndexOrder2(_orderId);
        address[] memory tokens = new address[](orderPartial[4]);
        for(uint i = 0; i < orderPartial[4]; i++){
            tokens[i] = olympusStorage.getIndexToken(_orderId, i);
        }
        return (
          orderPartial
        );
    }
    function updateIndexOrderToken(
        uint _orderId,
        address _tokenAddress,
        uint _actualPrice,
        uint _totalTokenAmount,
        uint _completedQuantity
    ) external allowProviderOnly(TypeDefinitions.ProviderType.Exchange) returns (bool success)
    {
        uint completedTokenAmount;
        uint tokenIndex;
        (completedTokenAmount, tokenIndex) = olympusStorage.getOrderTokenCompletedAmount(_orderId,_tokenAddress);
        ExchangeAdapterBase.OrderStatus status;
        if(completedTokenAmount == 0 && _completedQuantity < completedTokenAmount){
            status = ExchangeAdapterBase.OrderStatus.PartiallyCompleted;
        }
        if(_completedQuantity >= completedTokenAmount){
            status = ExchangeAdapterBase.OrderStatus.Completed;
        }
        olympusStorage.updateIndexOrderToken(_orderId, tokenIndex, _totalTokenAmount, _actualPrice, _completedQuantity, status);
        return true;
    }
    function updateOrderStatus(uint _orderId, StorageTypeDefinitions.OrderStatus _status)
        external allowProviderOnly(TypeDefinitions.ProviderType.Exchange)
        returns (bool success)
    {
        olympusStorage.updateOrderStatus(_orderId, _status);
        return true;
    }
    function getSubOrderStatus(uint _orderId, address _tokenAddress)
        external view returns (ExchangeAdapterBase.OrderStatus)
    {
        return exchangeProvider.getSubOrderStatus(_orderId, ERC20(_tokenAddress));
    }
    function adjustFee(uint _newFeePercentage) public onlyOwner returns (bool success) {
        require(_newFeePercentage < DENOMINATOR);
        feePercentage = _newFeePercentage;
        return true;
    }
    function adjustMOTFeeDiscount(uint _newDiscountPercentage) public onlyOwner returns(bool success) {
        require(_newDiscountPercentage <= 100);
        MOTDiscount = _newDiscountPercentage;
        return true;
    }
    function adjustTradeRange(uint _minInWei, uint _maxInWei) public onlyOwner returns (bool success) {
        require(_minInWei > 0);
        require(_maxInWei > _minInWei);
        minimumInWei = _minInWei;
        maximumInWei = _maxInWei;
        return true;
    }
    function getFeeAmount(uint amountInWei, bool feeIsMOT) private view returns (uint){
        if(feeIsMOT){
            return ((amountInWei * feePercentage / DENOMINATOR) * (100 - MOTDiscount)) / 100;
        } else {
            return amountInWei * feePercentage / DENOMINATOR;
        }
    }
    function payFee(uint totalValue, uint feeValueInETH, address sender, bool feeIsMOT) private returns (uint){
        if(feeIsMOT){
            uint MOTPrice;
            uint allowance = MOT.allowance(sender,address(this));
            (MOTPrice,) = priceProvider.getRates(address(MOT), feeValueInETH);
            uint amount = (feeValueInETH * MOTPrice) / 10**18;
            require(allowance >= amount);
            require(MOT.transferFrom(sender,address(this),amount));
            return totalValue; 
        } else { 
            return totalValue - feeValueInETH;
        }
    }
    function withdrawERC20(address receiveAddress,address _tokenAddress) public onlyOwner returns(bool success)
    {
        uint _balance = ERC20(_tokenAddress).balanceOf(address(this));
        require(_tokenAddress != 0x0 && receiveAddress != 0x0 && _balance != 0);
        require(ERC20(_tokenAddress).transfer(receiveAddress,_balance));
        return true;
    }
    function withdrawETH(address receiveAddress) public onlyOwner returns(bool success)
    {
        require(receiveAddress != 0x0);
        receiveAddress.transfer(this.balance);
        return true;
    }
}
```

## RQ1_ca7edc2ef72f

SHA-256 `26992481c3c873bf07fbcda3eb1af8d0b21fa8315153bba876ec844b6778a1dc`

```solidity
pragma solidity ^0.4.23;
interface ApproveAndCallFallBack {
    function receiveApproval(
        address from,
        uint256 _amount,
        address _token,
        bytes _data
    ) external;
}
contract Controlled {
    modifier onlyController { 
        require(msg.sender == controller); 
        _; 
    }
    address public controller;
    constructor() internal { 
        controller = msg.sender; 
    }
    function changeController(address _newController) public onlyController {
        controller = _newController;
    }
}
library RLPReader {
    uint8 constant STRING_SHORT_START = 0x80;
    uint8 constant STRING_LONG_START  = 0xb8;
    uint8 constant LIST_SHORT_START   = 0xc0;
    uint8 constant LIST_LONG_START    = 0xf8;
    uint8 constant WORD_SIZE = 32;
    struct RLPItem {
        uint len;
        uint memPtr;
    }
    function toRlpItem(bytes memory item) internal pure returns (RLPItem memory) {
        if (item.length == 0) 
            return RLPItem(0, 0);
        uint memPtr;
        assembly {
            memPtr := add(item, 0x20)
        }
        return RLPItem(item.length, memPtr);
    }
    function toList(RLPItem memory item) internal pure returns (RLPItem[] memory result) {
        require(isList(item));
        uint items = numItems(item);
        result = new RLPItem[](items);
        uint memPtr = item.memPtr + _payloadOffset(item.memPtr);
        uint dataLen;
        for (uint i = 0; i < items; i++) {
            dataLen = _itemLength(memPtr);
            result[i] = RLPItem(dataLen, memPtr); 
            memPtr = memPtr + dataLen;
        }
    }
    function isList(RLPItem memory item) internal pure returns (bool) {
        uint8 byte0;
        uint memPtr = item.memPtr;
        assembly {
            byte0 := byte(0, mload(memPtr))
        }
        if (byte0 < LIST_SHORT_START)
            return false;
        return true;
    }
    function numItems(RLPItem memory item) internal pure returns (uint) {
        uint count = 0;
        uint currPtr = item.memPtr + _payloadOffset(item.memPtr);
        uint endPtr = item.memPtr + item.len;
        while (currPtr < endPtr) {
           currPtr = currPtr + _itemLength(currPtr); 
           count++;
        }
        return count;
    }
    function _itemLength(uint memPtr) internal pure returns (uint len) {
        uint byte0;
        assembly {
            byte0 := byte(0, mload(memPtr))
        }
        if (byte0 < STRING_SHORT_START)
            return 1;
        else if (byte0 < STRING_LONG_START)
            return byte0 - STRING_SHORT_START + 1;
        else if (byte0 < LIST_SHORT_START) {
            assembly {
                let byteLen := sub(byte0, 0xb7) 
                memPtr := add(memPtr, 1) 
                let dataLen := div(mload(memPtr), exp(256, sub(32, byteLen))) 
                len := add(dataLen, add(byteLen, 1))
            }
        }
        else if (byte0 < LIST_LONG_START) {
            return byte0 - LIST_SHORT_START + 1;
        } 
        else {
            assembly {
                let byteLen := sub(byte0, 0xf7)
                memPtr := add(memPtr, 1)
                let dataLen := div(mload(memPtr), exp(256, sub(32, byteLen))) 
                len := add(dataLen, add(byteLen, 1))
            }
        }
    }
    function _payloadOffset(uint memPtr) internal pure returns (uint) {
        uint byte0;
        assembly {
            byte0 := byte(0, mload(memPtr))
        }
        if (byte0 < STRING_SHORT_START) 
            return 0;
        else if (byte0 < STRING_LONG_START || (byte0 >= LIST_SHORT_START && byte0 < LIST_LONG_START))
            return 1;
        else if (byte0 < LIST_SHORT_START)  
            return byte0 - (STRING_LONG_START - 1) + 1;
        else
            return byte0 - (LIST_LONG_START - 1) + 1;
    }
    function toBoolean(RLPItem memory item) internal pure returns (bool) {
        require(item.len == 1, "Invalid RLPItem. Booleans are encoded in 1 byte");
        uint result;
        uint memPtr = item.memPtr;
        assembly {
            result := byte(0, mload(memPtr))
        }
        return result == 0 ? false : true;
    }
    function toAddress(RLPItem memory item) internal pure returns (address) {
        require(item.len == 21, "Invalid RLPItem. Addresses are encoded in 20 bytes");
        uint memPtr = item.memPtr + 1; 
        uint addr;
        assembly {
            addr := div(mload(memPtr), exp(256, 12)) 
        }
        return address(addr);
    }
    function toUint(RLPItem memory item) internal pure returns (uint) {
        uint offset = _payloadOffset(item.memPtr);
        uint len = item.len - offset;
        uint memPtr = item.memPtr + offset;
        uint result;
        assembly {
            result := div(mload(memPtr), exp(256, sub(32, len))) 
        }
        return result;
    }
    function toBytes(RLPItem memory item) internal pure returns (bytes) {
        uint offset = _payloadOffset(item.memPtr);
        uint len = item.len - offset; 
        bytes memory result = new bytes(len);
        uint destPtr;
        assembly {
            destPtr := add(0x20, result)
        }
        copy(item.memPtr + offset, destPtr, len);
        return result;
    }
    function copy(uint src, uint dest, uint len) internal pure {
        for (; len >= WORD_SIZE; len -= WORD_SIZE) {
            assembly {
                mstore(dest, mload(src))
            }
            src += WORD_SIZE;
            dest += WORD_SIZE;
        }
        uint mask = 256 ** (WORD_SIZE - len) - 1;
        assembly {
            let srcpart := and(mload(src), not(mask)) 
            let destpart := and(mload(dest), mask) 
            mstore(dest, or(destpart, srcpart))
        }
    }
}
contract RLPHelper {
    using RLPReader for bytes;
    using RLPReader for uint;
    using RLPReader for RLPReader.RLPItem;
    function isList(bytes memory item) public pure returns (bool) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.isList();
    }
    function itemLength(bytes memory item) public pure returns (uint) {
        uint memPtr;
        assembly {
            memPtr := add(0x20, item)
        }
        return memPtr._itemLength();
    }
    function numItems(bytes memory item) public pure returns (uint) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.numItems();
    }
    function toBytes(bytes memory item) public pure returns (bytes) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toBytes();
    }
    function toUint(bytes memory item) public pure returns (uint) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toUint();
    }
    function toAddress(bytes memory item) public pure returns (address) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toAddress();
    }
    function toBoolean(bytes memory item) public pure returns (bool) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return rlpItem.toBoolean();
    }
    function bytesToString(bytes memory item) public pure returns (string) {
        RLPReader.RLPItem memory rlpItem = item.toRlpItem();
        return string(rlpItem.toBytes());
    }
    function pollTitle(bytes memory item) public pure returns (string) {
        RLPReader.RLPItem[] memory items = item.toRlpItem().toList();
        return string(items[0].toBytes());
    }
    function pollBallot(bytes memory item, uint ballotNum) public pure returns (string) {
        RLPReader.RLPItem[] memory items = item.toRlpItem().toList();
        items = items[1].toList();
        return string(items[ballotNum].toBytes());
    }
}
interface TokenController {
    function proxyPayment(address _owner) external payable returns(bool);
    function onTransfer(address _from, address _to, uint _amount) external returns(bool);
    function onApprove(address _owner, address _spender, uint _amount) external
        returns(bool);
}
interface ERC20Token {
    function transfer(address _to, uint256 _value) external returns (bool success);
    function approve(address _spender, uint256 _value) external returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) external returns (bool success);
    function balanceOf(address _owner) external view returns (uint256 balance);
    function allowance(address _owner, address _spender) external view returns (uint256 remaining);
    function totalSupply() external view returns (uint256 supply);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract MiniMeTokenInterface is ERC20Token {
    function approveAndCall(
        address _spender,
        uint256 _amount,
        bytes _extraData
    ) 
        external 
        returns (bool success);
    function createCloneToken(
        string _cloneTokenName,
        uint8 _cloneDecimalUnits,
        string _cloneTokenSymbol,
        uint _snapshotBlock,
        bool _transfersEnabled
    ) 
        public
        returns(address);
    function generateTokens(
        address _owner,
        uint _amount
    )
        public
        returns (bool);
    function destroyTokens(
        address _owner,
        uint _amount
    ) 
        public
        returns (bool);
    function enableTransfers(bool _transfersEnabled) public;
    function claimTokens(address _token) public;
    function balanceOfAt(
        address _owner,
        uint _blockNumber
    ) 
        public
        constant
        returns (uint);
    function totalSupplyAt(uint _blockNumber) public view returns(uint);
}
contract MiniMeTokenFactory {
    function createCloneToken(
        address _parentToken,
        uint _snapshotBlock,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        bool _transfersEnabled
    ) public returns (MiniMeToken) {
        MiniMeToken newToken = new MiniMeToken(
            this,
            _parentToken,
            _snapshotBlock,
            _tokenName,
            _decimalUnits,
            _tokenSymbol,
            _transfersEnabled
            );
        newToken.changeController(msg.sender);
        return newToken;
    }
}
contract MiniMeToken is MiniMeTokenInterface, Controlled {
    string public name;                
    uint8 public decimals;             
    string public symbol;              
    string public version = "MMT_0.1"; 
    struct Checkpoint {
        uint128 fromBlock;
        uint128 value;
    }
    MiniMeToken public parentToken;
    uint public parentSnapShotBlock;
    uint public creationBlock;
    mapping (address => Checkpoint[]) balances;
    mapping (address => mapping (address => uint256)) allowed;
    Checkpoint[] totalSupplyHistory;
    bool public transfersEnabled;
    MiniMeTokenFactory public tokenFactory;
    constructor(
        address _tokenFactory,
        address _parentToken,
        uint _parentSnapShotBlock,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        bool _transfersEnabled
    ) 
        public
    {
        require(_tokenFactory != address(0)); 
        tokenFactory = MiniMeTokenFactory(_tokenFactory);
        name = _tokenName;                                 
        decimals = _decimalUnits;                          
        symbol = _tokenSymbol;                             
        parentToken = MiniMeToken(_parentToken);
        parentSnapShotBlock = _parentSnapShotBlock;
        transfersEnabled = _transfersEnabled;
        creationBlock = block.number;
    }
    function transfer(address _to, uint256 _amount) public returns (bool success) {
        require(transfersEnabled);
        return doTransfer(msg.sender, _to, _amount);
    }
    function transferFrom(
        address _from,
        address _to,
        uint256 _amount
    ) 
        public 
        returns (bool success)
    {
        if (msg.sender != controller) {
            require(transfersEnabled);
            if (allowed[_from][msg.sender] < _amount) { 
                return false;
            }
            allowed[_from][msg.sender] -= _amount;
        }
        return doTransfer(_from, _to, _amount);
    }
    function doTransfer(
        address _from,
        address _to,
        uint _amount
    ) 
        internal
        returns(bool)
    {
        if (_amount == 0) {
            return true;
        }
        require(parentSnapShotBlock < block.number);
        require((_to != 0) && (_to != address(this)));
        uint256 previousBalanceFrom = balanceOfAt(_from, block.number);
        if (previousBalanceFrom < _amount) {
            return false;
        }
        if (isContract(controller)) {
            require(TokenController(controller).onTransfer(_from, _to, _amount));
        }
        updateValueAtNow(balances[_from], previousBalanceFrom - _amount);
        uint256 previousBalanceTo = balanceOfAt(_to, block.number);
        require(previousBalanceTo + _amount >= previousBalanceTo); 
        updateValueAtNow(balances[_to], previousBalanceTo + _amount);
        emit Transfer(_from, _to, _amount);
        return true;
    }
    function doApprove(
        address _from,
        address _spender,
        uint256 _amount
    )
        internal 
        returns (bool)
    {
        require(transfersEnabled);
        require((_amount == 0) || (allowed[_from][_spender] == 0));
        if (isContract(controller)) {
            require(TokenController(controller).onApprove(_from, _spender, _amount));
        }
        allowed[_from][_spender] = _amount;
        emit Approval(_from, _spender, _amount);
        return true;
    }
    function balanceOf(address _owner) external view returns (uint256 balance) {
        return balanceOfAt(_owner, block.number);
    }
    function approve(address _spender, uint256 _amount) external returns (bool success) {
        doApprove(msg.sender, _spender, _amount);
    }
    function allowance(
        address _owner,
        address _spender
    ) 
        external
        view
        returns (uint256 remaining)
    {
        return allowed[_owner][_spender];
    }
    function approveAndCall(
        address _spender,
        uint256 _amount,
        bytes _extraData
    ) 
        external 
        returns (bool success)
    {
        require(doApprove(msg.sender, _spender, _amount));
        ApproveAndCallFallBack(_spender).receiveApproval(
            msg.sender,
            _amount,
            this,
            _extraData
        );
        return true;
    }
    function totalSupply() external view returns (uint) {
        return totalSupplyAt(block.number);
    }
    function balanceOfAt(
        address _owner,
        uint _blockNumber
    ) 
        public
        view
        returns (uint) 
    {
        if ((balances[_owner].length == 0) || (balances[_owner][0].fromBlock > _blockNumber)) {
            if (address(parentToken) != 0) {
                return parentToken.balanceOfAt(_owner, min(_blockNumber, parentSnapShotBlock));
            } else {
                return 0;
            }
        } else {
            return getValueAt(balances[_owner], _blockNumber);
        }
    }
    function totalSupplyAt(uint _blockNumber) public view returns(uint) {
        if ((totalSupplyHistory.length == 0) || (totalSupplyHistory[0].fromBlock > _blockNumber)) {
            if (address(parentToken) != 0) {
                return parentToken.totalSupplyAt(min(_blockNumber, parentSnapShotBlock));
            } else {
                return 0;
            }
        } else {
            return getValueAt(totalSupplyHistory, _blockNumber);
        }
    }
    function createCloneToken(
        string _cloneTokenName,
        uint8 _cloneDecimalUnits,
        string _cloneTokenSymbol,
        uint _snapshotBlock,
        bool _transfersEnabled
        ) 
            public
            returns(address)
        {
        uint snapshotBlock = _snapshotBlock;
        if (snapshotBlock == 0) {
            snapshotBlock = block.number;
        }
        MiniMeToken cloneToken = tokenFactory.createCloneToken(
            this,
            snapshotBlock,
            _cloneTokenName,
            _cloneDecimalUnits,
            _cloneTokenSymbol,
            _transfersEnabled
            );
        cloneToken.changeController(msg.sender);
        emit NewCloneToken(address(cloneToken), snapshotBlock);
        return address(cloneToken);
    }
    function generateTokens(
        address _owner,
        uint _amount
    )
        public
        onlyController
        returns (bool)
    {
        uint curTotalSupply = totalSupplyAt(block.number);
        require(curTotalSupply + _amount >= curTotalSupply); 
        uint previousBalanceTo = balanceOfAt(_owner, block.number);
        require(previousBalanceTo + _amount >= previousBalanceTo); 
        updateValueAtNow(totalSupplyHistory, curTotalSupply + _amount);
        updateValueAtNow(balances[_owner], previousBalanceTo + _amount);
        emit Transfer(0, _owner, _amount);
        return true;
    }
    function destroyTokens(
        address _owner,
        uint _amount
    ) 
        public
        onlyController
        returns (bool)
    {
        uint curTotalSupply = totalSupplyAt(block.number);
        require(curTotalSupply >= _amount);
        uint previousBalanceFrom = balanceOfAt(_owner, block.number);
        require(previousBalanceFrom >= _amount);
        updateValueAtNow(totalSupplyHistory, curTotalSupply - _amount);
        updateValueAtNow(balances[_owner], previousBalanceFrom - _amount);
        emit Transfer(_owner, 0, _amount);
        return true;
    }
    function enableTransfers(bool _transfersEnabled) public onlyController {
        transfersEnabled = _transfersEnabled;
    }
    function getValueAt(
        Checkpoint[] storage checkpoints,
        uint _block
    ) 
        view
        internal
        returns (uint)
    {
        if (checkpoints.length == 0) {
            return 0;
        }
        if (_block >= checkpoints[checkpoints.length-1].fromBlock) {
            return checkpoints[checkpoints.length-1].value;
        }
        if (_block < checkpoints[0].fromBlock) {
            return 0;
        }
        uint min = 0;
        uint max = checkpoints.length-1;
        while (max > min) {
            uint mid = (max + min + 1) / 2;
            if (checkpoints[mid].fromBlock<=_block) {
                min = mid;
            } else {
                max = mid-1;
            }
        }
        return checkpoints[min].value;
    }
    function updateValueAtNow(Checkpoint[] storage checkpoints, uint _value) internal {
        if (
            (checkpoints.length == 0) ||
            (checkpoints[checkpoints.length - 1].fromBlock < block.number)) 
        {
            Checkpoint storage newCheckPoint = checkpoints[checkpoints.length++];
            newCheckPoint.fromBlock = uint128(block.number);
            newCheckPoint.value = uint128(_value);
        } else {
            Checkpoint storage oldCheckPoint = checkpoints[checkpoints.length-1];
            oldCheckPoint.value = uint128(_value);
        }
    }
    function isContract(address _addr) internal view returns(bool) {
        uint size;
        if (_addr == 0) {
            return false;
        }    
        assembly {
            size := extcodesize(_addr)
        }
        return size > 0;
    }
    function min(uint a, uint b) internal returns (uint) {
        return a < b ? a : b;
    }
    function () public payable {
        require(isContract(controller));
        require(TokenController(controller).proxyPayment.value(msg.value)(msg.sender));
    }
    function claimTokens(address _token) public onlyController {
        if (_token == 0x0) {
            controller.transfer(address(this).balance);
            return;
        }
        MiniMeToken token = MiniMeToken(_token);
        uint balance = token.balanceOf(address(this));
        token.transfer(controller, balance);
        emit ClaimedTokens(_token, controller, balance);
    }
    event ClaimedTokens(address indexed _token, address indexed _controller, uint _amount);
    event Transfer(address indexed _from, address indexed _to, uint256 _amount);
    event NewCloneToken(address indexed _cloneToken, uint snapshotBlock);
    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _amount
    );
}
contract PollManager is Controlled {
    struct Poll {
        uint startBlock;
        uint endBlock;
        bool canceled;
        uint voters;
        bytes description;
        uint8 numBallots;
        mapping(uint8 => mapping(address => uint)) ballots;
        mapping(uint8 => uint) qvResults;
        mapping(uint8 => uint) results;
        address author;
    }
    Poll[] _polls;
    MiniMeToken public token;
    RLPHelper public rlpHelper;
    constructor(address _token) 
        public {
        token = MiniMeToken(_token);
        rlpHelper = new RLPHelper();
    }
    modifier onlySNTHolder {
        require(token.balanceOf(msg.sender) > 0, "SNT Balance is required to perform this operation"); 
        _; 
    }
    function addPoll(
        uint _endBlock,
        bytes _description,
        uint8 _numBallots)
        public
        onlySNTHolder
        returns (uint _idPoll)
    {
        _idPoll = addPoll(block.number, _endBlock, _description, _numBallots);
    }
    function addPoll(
        uint _startBlock,
        uint _endBlock,
        bytes _description,
        uint8 _numBallots)
        public
        onlySNTHolder
        returns (uint _idPoll)
    {
        require(_endBlock > block.number, "End block must be greater than current block");
        require(_startBlock >= block.number && _startBlock < _endBlock, "Start block must not be in the past, and should be less than the end block" );
        require(_numBallots <= 15, "Only a max of 15 ballots are allowed");
        _idPoll = _polls.length;
        _polls.length ++;
        Poll storage p = _polls[_idPoll];
        p.startBlock = _startBlock;
        p.endBlock = _endBlock;
        p.voters = 0;
        p.numBallots = _numBallots;
        p.description = _description;
        p.author = msg.sender;
        emit PollCreated(_idPoll); 
    }
    function updatePollDescription(
        uint _idPoll, 
        bytes _description,
        uint8 _numBallots)
        public
    {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        require(_numBallots <= 15, "Only a max of 15 ballots are allowed");
        Poll storage p = _polls[_idPoll];
        require(p.startBlock > block.number, "You cannot modify an active poll");
        require(p.author == msg.sender || msg.sender == controller, "Only the owner/controller can modify the poll");
        p.numBallots = _numBallots;
        p.description = _description;
        p.author = msg.sender;
    }
    function cancelPoll(uint _idPoll) 
        public {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        require(!p.canceled, "Poll has been canceled already");
        require(p.endBlock > block.number, "Only active polls can be canceled");
        if(p.startBlock < block.number){
            require(msg.sender == controller, "Only the controller can cancel the poll");
        } else {
            require(p.author == msg.sender, "Only the owner can cancel the poll");
        }
        p.canceled = true;
        emit PollCanceled(_idPoll);
    }
    function canVote(uint _idPoll) 
        public 
        view 
        returns(bool)
    {
        if(_idPoll >= _polls.length) return false;
        Poll storage p = _polls[_idPoll];
        uint balance = token.balanceOfAt(msg.sender, p.startBlock);
        return block.number >= p.startBlock && block.number < p.endBlock && !p.canceled && balance != 0;
    }
    function sqrt(uint256 x) public pure returns (uint256 y) {
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
    function vote(uint _idPoll, uint[] _ballots) public {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        require(block.number >= p.startBlock && block.number < p.endBlock && !p.canceled, "Poll is inactive");
        require(_ballots.length == p.numBallots, "Number of ballots is incorrect");
        unvote(_idPoll);
        uint amount = token.balanceOfAt(msg.sender, p.startBlock);
        require(amount != 0, "No SNT balance available at start block of poll");
        p.voters++;
        uint totalBallots = 0;
        for(uint8 i = 0; i < _ballots.length; i++){
            totalBallots += _ballots[i];
            p.ballots[i][msg.sender] = _ballots[i];
            if(_ballots[i] != 0){
                p.qvResults[i] += sqrt(_ballots[i] / 1 ether);
                p.results[i] += _ballots[i];
            }
        }
        require(totalBallots <= amount, "Total ballots must be less than the SNT balance at poll start block");
        emit Vote(_idPoll, msg.sender, _ballots);
    }
    function unvote(uint _idPoll) public {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        require(block.number >= p.startBlock && block.number < p.endBlock && !p.canceled, "Poll is inactive");
        if(p.voters == 0) return;
        p.voters--;
        for(uint8 i = 0; i < p.numBallots; i++){
            uint ballotAmount = p.ballots[i][msg.sender];
            p.ballots[i][msg.sender] = 0;
            if(ballotAmount != 0){
                p.qvResults[i] -= sqrt(ballotAmount / 1 ether);
                p.results[i] -= ballotAmount;
            }
        }
        emit Unvote(_idPoll, msg.sender);
    }
    function nPolls()
        public
        view 
        returns(uint)
    {
        return _polls.length;
    }
    function poll(uint _idPoll)
        public 
        view 
        returns(
        uint _startBlock,
        uint _endBlock,
        bool _canVote,
        bool _canceled,
        bytes _description,
        uint8 _numBallots,
        bool _finalized,
        uint _voters,
        address _author,
        uint[15] _tokenTotal,
        uint[15] _quadraticVotes
    )
    {
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        _startBlock = p.startBlock;
        _endBlock = p.endBlock;
        _canceled = p.canceled;
        _canVote = canVote(_idPoll);
        _description = p.description;
        _numBallots = p.numBallots;
        _author = p.author;
        _finalized = (!p.canceled) && (block.number >= _endBlock);
        _voters = p.voters;
        for(uint8 i = 0; i < p.numBallots; i++){
            _tokenTotal[i] = p.results[i];
            _quadraticVotes[i] = p.qvResults[i];
        }
    }
    function pollTitle(uint _idPoll) public view returns (string){
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll memory p = _polls[_idPoll];
        return rlpHelper.pollTitle(p.description);
    }
    function pollBallot(uint _idPoll, uint _ballot) public view returns (string){
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll memory p = _polls[_idPoll];
        return rlpHelper.pollBallot(p.description, _ballot);
    }
    function getVote(uint _idPoll, address _voter) 
        public 
        view 
        returns (uint[15] votes){
        require(_idPoll < _polls.length, "Invalid _idPoll");
        Poll storage p = _polls[_idPoll];
        for(uint8 i = 0; i < p.numBallots; i++){
            votes[i] = p.ballots[i][_voter];
        }
        return votes;
    }
    event Vote(uint indexed idPoll, address indexed _voter, uint[] ballots);
    event Unvote(uint indexed idPoll, address indexed _voter);
    event PollCanceled(uint indexed idPoll);
    event PollCreated(uint indexed idPoll);
}
```

## RQ1_0da822a515f7

SHA-256 `5e3589e867742b38d9e358bf9bd8cf7638a3eb0518697e910a4f929573ab0e0b`

```solidity
pragma solidity ^0.4.19;
contract CovestingToken {
    string public name = "COVESTING";
    string public symbol = "COV";
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
    function CovestingToken() public {
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

## RQ1_f06c9922dd0c

SHA-256 `bd472593d7ec968b61448ce0f67d5fe968ac0acf4b924a51402f57df49c4b70a`

```solidity
pragma solidity ^0.4.22;
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
interface Token { 
    function distr(address _to, uint256 _value) external returns (bool);
    function totalSupply() constant external returns (uint256 supply);
    function balanceOf(address _owner) constant external returns (uint256 balance);
}
contract TrueTone_network is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "TrueTone_network";
    string public constant symbol = "TTN";
    uint public constant decimals = 18;
    uint256 public totalSupply = 25000000000e18;
    uint256 public totalDistributed = 25000000000e18;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value = 25000000000e18;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Distr(address indexed to, uint256 amount);
    event DistrFinished();
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
    modifier onlyWhitelist() {
        require(blacklist[msg.sender] == false);
        _;
    }
    function TodaNetwork() public {
        owner = msg.sender;
        balances[owner] = totalDistributed;
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
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Distr(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function () external payable {
        getTokens();
     }
    function getTokens() payable canDistr onlyWhitelist public {
        if (value > totalRemaining) {
            value = totalRemaining;
        }
        require(value <= totalRemaining);
        address investor = msg.sender;
        uint256 toGive = value;
        distr(investor, toGive);
        if (toGive > 0) {
            blacklist[investor] = true;
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
        value = value.div(5000).mul(5000);
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
        uint256 etherBalance = address(this).balance;
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

## RQ1_4b70decadc18

SHA-256 `1f3982306077ae18de8dfd9c4cfd32f9510253440d338258624d1ea2ae739c63`

```solidity
contract Private_Fund{
    address public beneficiary;
    uint public amountRaised;
    uint256 public start;
    uint256 public deadline;
    address public creator;
    bool public deadline_status = false;
    Funder[] public funders;
    event FundTransfer(address backer, uint amount, bool isContribution);
    struct Funder {
        address addr;
        uint amount;
    }
    modifier onlyCreator() {
        if (creator != msg.sender) {
            throw;
        }
        _;
     }
    modifier afterDeadline() { if (now >= deadline) _;}
    function check_deadline() {
      if (now >= deadline) deadline_status = true;
      else                 deadline_status = false;
    }
    function deadline_modify(uint256 _start ,uint256 _duration) onlyCreator {
       start = _start;
       deadline = _start + _duration * 1 days; 
    }
    function Private_Fund(address _creator, address _beneficiary, uint256 _duration) {
        creator = _creator;
        beneficiary = _beneficiary;
        start = now;
        deadline = start + _duration * 1 minutes;
    }   
    function () payable {
        if(now < start) throw;
        if(now >= deadline) throw;
        uint amount = msg.value;
        funders[funders.length++] = Funder({addr: msg.sender, amount: amount});
        amountRaised += amount;
        FundTransfer(msg.sender, amount, true);
    }
    function withdraw_privatefund(bool _withdraw_en) afterDeadline onlyCreator{
        if (_withdraw_en){
            beneficiary.send(amountRaised);
            FundTransfer(beneficiary, amountRaised, false);
        } else {
            FundTransfer(0, 11, false);
            for (uint i = 0; i < funders.length; ++i) {
              funders[i].addr.send(funders[i].amount);  
              FundTransfer(funders[i].addr, funders[i].amount, false);
            }               
        }
    }
    function kill() {
      suicide(beneficiary);
    }
}
```

## RQ1_277940cef55d

SHA-256 `1eb58ac73307f8aac7a8c52f6dfe47b53b2f5fccfbce4f3af94d71e6f5a8d742`

```solidity
pragma solidity ^0.4.23;
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
contract BankingPay is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "BankingPay";
    string public constant symbol = "BKP";
    uint public constant decimals = 8;
    uint256 public totalSupply = 3000000000e8;
    uint256 public totalDistributed =  500000000e8;    
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public tokensPerEth = 10000000e8;
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
    function BankingPayToken () public {
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

## RQ1_dd26f3dfb5a6

SHA-256 `c3dc3547bc518576a052626496546c3d05c5f51b12e8de7e4f3cf0bfe1d6641b`

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
contract CLEIToken is ERC20Interface, AssetProxyInterface, Bytes32, ReturnData {
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
