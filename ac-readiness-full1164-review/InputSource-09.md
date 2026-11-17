# 本批实际输入源码

按输入原字节 SHA 核对。源码位置采用 UTF-8 字节偏移。

## RQ1_9b575cb4d0e1

SHA-256 `abde2cf2a8cee531519df7e0748c668c7ed371e8913507b6b7072a18057935fc`

```solidity
pragma solidity ^0.5.7;
interface RegistryInterface {
    function proxies(address) external view returns (address);
}
interface UserWalletInterface {
    function owner() external view returns (address);
}
interface TubInterface {
    function open() external returns (bytes32);
    function join(uint) external;
    function exit(uint) external;
    function lock(bytes32, uint) external;
    function free(bytes32, uint) external;
    function draw(bytes32, uint) external;
    function wipe(bytes32, uint) external;
    function give(bytes32, address) external;
    function shut(bytes32) external;
    function cups(bytes32) external view returns (address, uint, uint, uint);
    function gem() external view returns (ERC20Interface);
    function gov() external view returns (ERC20Interface);
    function skr() external view returns (ERC20Interface);
    function sai() external view returns (ERC20Interface);
    function ink(bytes32) external view returns (uint);
    function tab(bytes32) external returns (uint);
    function rap(bytes32) external returns (uint);
    function per() external view returns (uint);
    function pep() external view returns (PepInterface);
}
interface PepInterface {
    function peek() external returns (bytes32, bool);
}
interface ERC20Interface {
    function allowance(address, address) external view returns (uint);
    function balanceOf(address) external view returns (uint);
    function approve(address, uint) external;
    function transfer(address, uint) external returns (bool);
    function transferFrom(address, address, uint) external returns (bool);
    function deposit() external payable;
    function withdraw(uint) external;
}
interface UniswapExchange {
    function getEthToTokenOutputPrice(uint256 tokensBought) external view returns (uint256 ethSold);
    function getTokenToEthOutputPrice(uint256 ethBought) external view returns (uint256 tokensSold);
    function tokenToTokenSwapOutput(
        uint256 tokensBought,
        uint256 maxTokensSold,
        uint256 maxEthSold,
        uint256 deadline,
        address tokenAddr
        ) external returns (uint256  tokensSold);
}
interface CTokenInterface {
    function mint(uint mintAmount) external returns (uint); 
    function redeem(uint redeemTokens) external returns (uint);
    function redeemUnderlying(uint redeemAmount) external returns (uint);
    function exchangeRateCurrent() external returns (uint);
    function transfer(address, uint) external returns (bool);
    function transferFrom(address, address, uint) external returns (bool);
    function balanceOf(address) external view returns (uint);
}
interface CETHInterface {
    function mint() external payable; 
    function transfer(address, uint) external returns (bool);
}
interface CDAIInterface {
    function mint(uint mintAmount) external returns (uint); 
    function repayBorrowBehalf(address borrower, uint repayAmount) external returns (uint);
    function borrowBalanceCurrent(address account) external returns (uint);
}
contract DSMath {
    function add(uint x, uint y) internal pure returns (uint z) {
        require((z = x + y) >= x, "math-not-safe");
    }
    function mul(uint x, uint y) internal pure returns (uint z) {
        require(y == 0 || (z = x * y) / y == x, "math-not-safe");
    }
    uint constant WAD = 10 ** 18;
    uint constant RAY = 10 ** 27;
    function rmul(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, y), RAY / 2) / RAY;
    }
    function rdiv(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, RAY), y / 2) / y;
    }
    function wmul(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, y), WAD / 2) / WAD;
    }
    function wdiv(uint x, uint y) internal pure returns (uint z) {
        z = add(mul(x, WAD), y / 2) / y;
    }
}
contract Helper is DSMath {
    address public ethAddr = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    address public daiAddr = 0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359;
    address public registry = 0x498b3BfaBE9F73db90D252bCD4Fa9548Cd0Fd981;
    address public sai = 0x448a5065aeBB8E423F0896E6c5D525C040f59af3;
    address public ume = 0x2C4Bd064b998838076fa341A83d007FC2FA50957; 
    address public ude = 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14; 
    address public cEth = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address public cDai = 0xF5DCe57282A584D2746FaF1593d3121Fcac444dC;
    function setApproval(address erc20, uint srcAmt, address to) internal {
        ERC20Interface erc20Contract = ERC20Interface(erc20);
        uint tokenAllowance = erc20Contract.allowance(address(this), to);
        if (srcAmt > tokenAllowance) {
            erc20Contract.approve(to, 2**255);
        }
    }
    function setAllowance(ERC20Interface _token, address _spender) internal {
        if (_token.allowance(address(this), _spender) != uint(-1)) {
            _token.approve(_spender, uint(-1));
        }
    }
}
contract CompoundResolver is Helper {
    event LogMint(address erc20, address cErc20, uint tokenAmt, address owner);
    event LogRedeem(address erc20, address cErc20, uint tokenAmt, address owner);
    event LogBorrow(address erc20, address cErc20, uint tokenAmt, address owner);
    event LogRepay(address erc20, address cErc20, uint tokenAmt, address owner);
    function redeemUnderlying(address cErc20, uint tokenAmt) internal {
        if (tokenAmt > 0) {
            CTokenInterface cToken = CTokenInterface(cErc20);
            uint toBurn = cToken.balanceOf(address(this));
            uint tokenToReturn = wmul(toBurn, cToken.exchangeRateCurrent());
            tokenToReturn = tokenToReturn > tokenAmt ? tokenAmt : tokenToReturn;
            require(cToken.redeemUnderlying(tokenToReturn) == 0, "something went wrong");
        }
    }
    function mintCETH(uint ethAmt) internal {
        if (ethAmt > 0) {
            CETHInterface cToken = CETHInterface(cEth);
            cToken.mint.value(ethAmt)();
            uint cEthToReturn = wdiv(ethAmt, CTokenInterface(cEth).exchangeRateCurrent());
            cToken.transfer(msg.sender, cEthToReturn);
            emit LogMint(
                ethAddr,
                cEth,
                ethAmt,
                msg.sender
            );
        }
    }
    function mintCDAI(uint tokenAmt) internal {
        if (tokenAmt > 0) {
            ERC20Interface token = ERC20Interface(daiAddr);
            uint toDeposit = token.balanceOf(msg.sender);
            toDeposit = toDeposit > tokenAmt ? tokenAmt : toDeposit;
            token.transferFrom(msg.sender, address(this), toDeposit);
            CDAIInterface cToken = CDAIInterface(cDai);
            assert(cToken.mint(toDeposit) == 0);
            emit LogMint(
                daiAddr,
                cDai,
                tokenAmt,
                msg.sender
            );
        }
    }
    function fetchCETH(uint ethAmt) internal {
        if (ethAmt > 0) {
            CTokenInterface cToken = CTokenInterface(cEth);
            uint cTokenAmt = wdiv(ethAmt, cToken.exchangeRateCurrent());
            uint cEthBal = cToken.balanceOf(msg.sender);
            cTokenAmt = cEthBal >= cTokenAmt ? cTokenAmt : cTokenAmt - 1;
            require(ERC20Interface(cEth).transferFrom(msg.sender, address(this), cTokenAmt), "Contract Approved?");
        }
    }
    function checkCompound(uint ethAmt, uint daiAmt) internal returns (uint ethCol, uint daiDebt) {
        CTokenInterface cEthContract = CTokenInterface(cEth);
        uint cEthBal = cEthContract.balanceOf(address(this));
        uint ethExchangeRate = cEthContract.exchangeRateCurrent();
        ethCol = wmul(cEthBal, ethExchangeRate);
        ethCol = wdiv(ethCol, ethExchangeRate) <= cEthBal ? ethCol : ethCol - 1;
        if (ethCol > ethAmt) {
            ethCol = ethAmt;
        }
        daiDebt = CDAIInterface(cDai).borrowBalanceCurrent(msg.sender);
        if (daiDebt > daiAmt) {
            daiDebt = daiAmt;
        }
    }
}
contract MakerResolver is CompoundResolver {
    event LogOpen(uint cdpNum, address owner);
    event LogGive(uint cdpNum, address owner, address nextOwner);
    event LogLock(uint cdpNum, uint amtETH, uint amtPETH, address owner);
    event LogFree(uint cdpNum, uint amtETH, uint amtPETH, address owner);
    event LogDraw(uint cdpNum, uint amtDAI, address owner);
    event LogDrawSend(uint cdpNum, uint amtDAI, address to);
    event LogWipe(uint cdpNum, uint daiAmt, uint mkrFee, uint daiFee, address owner);
    event LogShut(uint cdpNum);
    function open() internal returns (uint) {
        bytes32 cup = TubInterface(sai).open();
        emit LogOpen(uint(cup), address(this));
        return uint(cup);
    }
    function give(uint cdpNum, address nextOwner) internal {
        TubInterface(sai).give(bytes32(cdpNum), nextOwner);
    }
    function wipe(uint cdpNum, uint _wad) internal returns (uint daiAmt) {
        if (_wad > 0) {
            TubInterface tub = TubInterface(sai);
            UniswapExchange daiEx = UniswapExchange(ude);
            UniswapExchange mkrEx = UniswapExchange(ume);
            ERC20Interface dai = tub.sai();
            ERC20Interface mkr = tub.gov();
            bytes32 cup = bytes32(cdpNum);
            (address lad,,,) = tub.cups(cup);
            require(lad == address(this), "cup-not-owned");
            setAllowance(dai, sai);
            setAllowance(mkr, sai);
            setAllowance(dai, ude);
            (bytes32 val, bool ok) = tub.pep().peek();
            uint mkrFee = wdiv(rmul(_wad, rdiv(tub.rap(cup), tub.tab(cup))), uint(val));
            uint daiFeeAmt = daiEx.getTokenToEthOutputPrice(mkrEx.getEthToTokenOutputPrice(mkrFee));
            daiAmt = add(_wad, daiFeeAmt);
            redeemUnderlying(cDai, daiAmt);
            if (ok && val != 0) {
                daiEx.tokenToTokenSwapOutput(
                    mkrFee,
                    daiAmt,
                    uint(999000000000000000000),
                    uint(1899063809), 
                    address(mkr)
                );
            }
            tub.wipe(cup, _wad);
            emit LogWipe(
                cdpNum,
                daiAmt,
                mkrFee,
                daiFeeAmt,
                address(this)
            );
        }
    }
    function free(uint cdpNum, uint jam) internal {
        if (jam > 0) {
            bytes32 cup = bytes32(cdpNum);
            address tubAddr = sai;
            TubInterface tub = TubInterface(tubAddr);
            ERC20Interface peth = tub.skr();
            ERC20Interface weth = tub.gem();
            uint ink = rdiv(jam, tub.per());
            ink = rmul(ink, tub.per()) <= jam ? ink : ink - 1;
            tub.free(cup, ink);
            setAllowance(peth, tubAddr);
            tub.exit(ink);
            uint freeJam = weth.balanceOf(address(this)); 
            weth.withdraw(freeJam);
            emit LogFree(
                cdpNum,
                freeJam,
                ink,
                address(this)
            );
        }
    }
    function lock(uint cdpNum, uint ethAmt) internal {
        if (ethAmt > 0) {
            bytes32 cup = bytes32(cdpNum);
            address tubAddr = sai;
            TubInterface tub = TubInterface(tubAddr);
            ERC20Interface weth = tub.gem();
            ERC20Interface peth = tub.skr();
            (address lad,,,) = tub.cups(cup);
            require(lad == address(this), "cup-not-owned");
            weth.deposit.value(ethAmt)();
            uint ink = rdiv(ethAmt, tub.per());
            ink = rmul(ink, tub.per()) <= ethAmt ? ink : ink - 1;
            setAllowance(weth, tubAddr);
            tub.join(ink);
            setAllowance(peth, tubAddr);
            tub.lock(cup, ink);
            emit LogLock(
                cdpNum,
                ethAmt,
                ink,
                address(this)
            );
        }
    }
    function draw(uint cdpNum, uint _wad) internal {
        bytes32 cup = bytes32(cdpNum);
        if (_wad > 0) {
            TubInterface tub = TubInterface(sai);
            tub.draw(cup, _wad);
            emit LogDraw(cdpNum, _wad, address(this));
        }
    }
    function getCDPStats(bytes32 cup) internal returns (uint ethCol, uint daiDebt) {
        TubInterface tub = TubInterface(sai);
        ethCol = rmul(tub.ink(cup), tub.per()); 
        daiDebt = tub.tab(cup);
    }
    function wipeAndFree(uint cdpNum, uint jam, uint _wad) internal returns (uint ethAmt, uint daiAmt) {
        (uint ethCol, uint daiDebt) = getCDPStats(bytes32(cdpNum));
        daiDebt = _wad < daiDebt ? _wad : daiDebt; 
        ethCol = jam < ethCol ? jam : ethCol; 
        daiAmt = wipe(cdpNum, daiDebt);
        ethAmt = ethCol;
        free(cdpNum, ethCol);
    }
    function lockAndDraw(uint cdpNum, uint jam, uint _wad) internal {
        lock(cdpNum, jam);
        draw(cdpNum, _wad);
    }
}
contract BridgeResolver is MakerResolver {
    function refillFunds(uint daiDebt) external {
        require(ERC20Interface(daiAddr).transferFrom(msg.sender, address(this),daiDebt), "Contract Approved?");
        mintCDAI(daiDebt);
    }
    function payUserDebt(uint daiDebt) internal {
        if (daiDebt > 0) {
            redeemUnderlying(cDai, daiDebt);
            require(CDAIInterface(cDai).repayBorrowBehalf(msg.sender, daiDebt) == 0, "Enough DAI?");
        }
    }
}
contract LiquidityProvider is BridgeResolver {
    mapping (address => uint) public deposits; 
    function depositDAI(uint amt) public {
        ERC20Interface(daiAddr).transferFrom(msg.sender, address(this), amt);
        CTokenInterface cToken = CTokenInterface(cDai);
        assert(cToken.mint(amt) == 0);
        uint cDaiAmt = wdiv(amt, cToken.exchangeRateCurrent());
        deposits[msg.sender] += cDaiAmt;
    }
    function withdrawDAI(uint amt) public {
        require(deposits[msg.sender] != 0, "Nothing to Withdraw");
        CTokenInterface cToken = CTokenInterface(cDai);
        uint withdrawAmt = wdiv(amt, cToken.exchangeRateCurrent());
        uint daiAmt = amt;
        if (withdrawAmt > deposits[msg.sender]) {
            withdrawAmt = deposits[msg.sender];
            daiAmt = wmul(withdrawAmt, cToken.exchangeRateCurrent());
        }
        require(cToken.redeem(withdrawAmt) == 0, "something went wrong");
        ERC20Interface(daiAddr).transfer(msg.sender, daiAmt);
        deposits[msg.sender] -= withdrawAmt;
    }
    function depositCDAI(uint amt) public {
        CTokenInterface cToken = CTokenInterface(cDai);
        require(cToken.transferFrom(msg.sender, address(this), amt) == true, "Nothing to deposit");
        deposits[msg.sender] += amt;
    }
    function withdrawCDAI(uint amt) public {
        require(deposits[msg.sender] != 0, "Nothing to Withdraw");
        CTokenInterface cToken = CTokenInterface(cDai);
        uint withdrawAmt = amt;
        if (withdrawAmt > deposits[msg.sender]) {
            withdrawAmt = deposits[msg.sender];
        }
        cToken.transfer(msg.sender, withdrawAmt);
        deposits[msg.sender] -= withdrawAmt;
    }
}
contract Bridge is LiquidityProvider {
    modifier isUserWallet {
        address userAdd = UserWalletInterface(msg.sender).owner();
        address walletAdd = RegistryInterface(registry).proxies(userAdd);
        require(walletAdd != address(0), "not-user-wallet");
        require(walletAdd == msg.sender, "not-wallet-owner");
        _;
    }
    function makerToCompound(uint cdpId, uint ethCol, uint daiDebt) public payable isUserWallet returns (uint daiAmt) {
        uint ethAmt;
        (ethAmt, daiAmt) = wipeAndFree(cdpId, ethCol, daiDebt);
        mintCETH(ethAmt);
        give(cdpId, msg.sender);
    }
    function compoundToMaker(uint cdpId, uint ethCol, uint daiDebt) public payable isUserWallet {
        (uint ethAmt, uint daiAmt) = checkCompound(ethCol, daiDebt);
        payUserDebt(daiAmt);
        fetchCETH(ethAmt);
        redeemUnderlying(cEth, ethAmt);
        uint cdpNum = cdpId > 0 ? cdpId : open();
        lockAndDraw(cdpNum, ethAmt, daiAmt);
        mintCDAI(daiAmt);
        give(cdpNum, msg.sender);
    }
}
contract MakerCompoundBridge is Bridge {
    constructor() public {
        setApproval(daiAddr, 10**30, cDai);
        setApproval(cDai, 10**30, cDai);
        setApproval(cEth, 10**30, cEth);
    }
    function() external payable {}
}
```

## RQ1_683cd65616eb

SHA-256 `8eaba1c06282ea6b81ca827c44b93fe935357790e7b10cef922d581000673e59`

```solidity
pragma solidity ^0.4.24;
contract fastum_1{
    uint public start = 6655475;
    modifier saleIsOn() {
    	require(block.number > start);
    	_;
    }
    address constant private PROMO = 0xA93c13B3E3561e5e2A1a20239486D03A16d1Fc4b;
    uint constant public MULTIPLIER = 115;
    uint constant public MAX_DEPOSIT = 1 ether;
    uint public currentReceiverIndex = 0; 
    uint public txnCount =0;
    uint public MIN_DEPOSIT = 0.01 ether;
    uint private PROMO_PERCENT = 15;
    uint constant public LAST_DEPOSIT_PERCENT = 10;
    LastDeposit public last;
    struct Deposit {
        address depositor; 
        uint128 deposit;   
        uint128 expect;    
    }
    struct LastDeposit {
        address depositor;
        uint expect;
        uint blockNumber;
    }
    Deposit[] private queue;
    function () saleIsOn private  payable {
        if(msg.value == 0 && msg.sender == last.depositor) {
            require(gasleft() >= 220000, "We require more gas!");
            require(last.blockNumber + 45 < block.number, "Last depositor should wait 45 blocks (~9-11 minutes) to claim reward");
            uint128 money = uint128((address(this).balance));
            if(money >= last.expect){
                last.depositor.transfer(last.expect);
            } else {
                last.depositor.transfer(money);
            }
            delete last;
        }
        else if(msg.value > 0){
            require(gasleft() >= 220000, "We require more gas!");
            require(msg.value <= MAX_DEPOSIT && msg.value >= MIN_DEPOSIT); 
            queue.push(Deposit(msg.sender, uint128(msg.value), uint128(msg.value*MULTIPLIER/100)));
            last.depositor = msg.sender;
            last.expect += msg.value*LAST_DEPOSIT_PERCENT/100;
            last.blockNumber = block.number;
            txnCount += 1;
            if(txnCount > 200) {
                MIN_DEPOSIT = 0.05 ether;
            } else if(txnCount > 150) {
                MIN_DEPOSIT = 0.04 ether;
            } else if(txnCount > 100) {
                MIN_DEPOSIT = 0.03 ether;
            }else if(txnCount > 50) {
                MIN_DEPOSIT = 0.02 ether;
            }else {
                MIN_DEPOSIT = 0.01 ether;
            }
            uint promo = msg.value*PROMO_PERCENT/100;
            uint128 contractBalance = uint128((address(this).balance));
            if(contractBalance >= promo){
                PROMO.transfer(promo);
            } else {
                PROMO.transfer(contractBalance);
            }
            pay();
        }
    }
    function pay() private {
        uint128 moneyCoefficient = uint128((address(this).balance)/last.expect);
        uint128 money = uint128((address(this).balance)-last.expect);
        if(moneyCoefficient < 1) {
            return;
        }
        for(uint i=0; i<queue.length; i++){
            uint idx = currentReceiverIndex + i;  
            Deposit storage dep = queue[idx]; 
            if(money >= dep.expect){  
                dep.depositor.transfer(dep.expect); 
                money -= dep.expect;            
                delete queue[idx];
            }else{
                dep.depositor.transfer(money); 
                dep.expect -= money;       
                break;
            }
            if(gasleft() <= 50000)        
                break;
        }
        currentReceiverIndex += i; 
    }
    function getDeposit(uint idx) public view returns (address depositor, uint deposit, uint expect){
        Deposit storage dep = queue[idx];
        return (dep.depositor, dep.deposit, dep.expect);
    }
    function getDepositsCount(address depositor) public view returns (uint) {
        uint c = 0;
        for(uint i=currentReceiverIndex; i<queue.length; ++i){
            if(queue[i].depositor == depositor)
                c++;
        }
        return c;
    }
    function getDeposits(address depositor) public view returns (uint[] idxs, uint128[] deposits, uint128[] expects) {
        uint c = getDepositsCount(depositor);
        idxs = new uint[](c);
        deposits = new uint128[](c);
        expects = new uint128[](c);
        if(c > 0) {
            uint j = 0;
            for(uint i=currentReceiverIndex; i<queue.length; ++i){
                Deposit storage dep = queue[i];
                if(dep.depositor == depositor){
                    idxs[j] = i;
                    deposits[j] = dep.deposit;
                    expects[j] = dep.expect;
                    j++;
                }
            }
        }
    }
}
```

## RQ1_9b691a13cbe7

SHA-256 `0caf920e93b4b84aa370eae2ec4979e40ed4d009e2073faf7f8695d78387e9ba`

```solidity
pragma solidity ^0.4.24;
contract Ethraffle {
    struct Contestant {
        address addr;
        uint raffleId;
    }
    event RaffleResult(
        uint indexed raffleId,
        uint winningNumber,
        address winningAddress,
        uint blockTimestamp,
        uint blockNumber,
        uint gasLimit,
        uint difficulty,
        uint gas,
        uint value,
        address msgSender,
        address blockCoinbase,
        bytes32 sha
    );
    event TicketPurchase(
        uint indexed raffleId,
        address contestant,
        uint number
    );
    event TicketRefund(
        uint indexed raffleId,
        address contestant,
        uint number
    );
    address public rakeAddress;
    uint constant public prize = 0.1 ether;
    uint constant public rake = 0.02 ether;
    uint constant public totalTickets = 6;
    uint constant public pricePerTicket = (prize + rake) / totalTickets;
    uint public raffleId = 1;
    uint public nextTicket = 1;
    mapping (uint => Contestant) public contestants;
    uint[] public gaps;
    function Ethraffle() public {
        rakeAddress = msg.sender;
    }
    function () payable public {
        buyTickets();
    }
    function buyTickets() payable public {
        uint moneySent = msg.value;
        while (moneySent >= pricePerTicket && nextTicket <= totalTickets) {
            uint currTicket = 0;
            if (gaps.length > 0) {
                currTicket = gaps[gaps.length-1];
                gaps.length--;
            } else {
                currTicket = nextTicket++;
            }
            contestants[currTicket] = Contestant(msg.sender, raffleId);
            TicketPurchase(raffleId, msg.sender, currTicket);
            moneySent -= pricePerTicket;
        }
        if (nextTicket > totalTickets) {
            chooseWinner();
        }
        if (moneySent > 0) {
            msg.sender.transfer(moneySent);
        }
    }
    function chooseWinner() private {
        bytes32 sha = sha3(
            block.timestamp,
            block.number,
            block.gaslimit,
            block.difficulty,
            msg.gas,
            msg.value,
            msg.sender,
            block.coinbase
        );
        uint winningNumber = (uint(sha) % totalTickets) + 1;
        address winningAddress = contestants[winningNumber].addr;
        RaffleResult(
            raffleId, winningNumber, winningAddress, block.timestamp,
            block.number, block.gaslimit, block.difficulty, msg.gas,
            msg.value, msg.sender, block.coinbase, sha
        );
        raffleId++;
        nextTicket = 1;
        winningAddress.transfer(prize);
        rakeAddress.transfer(rake);
    }
    function getRefund() public {
        uint refunds = 0;
        for (uint i = 1; i <= totalTickets; i++) {
            if (msg.sender == contestants[i].addr && raffleId == contestants[i].raffleId) {
                refunds++;
                contestants[i] = Contestant(address(0), 0);
                gaps.push(i);
                TicketRefund(raffleId, msg.sender, i);
            }
        }
        if (refunds > 0) {
            msg.sender.transfer(refunds * pricePerTicket);
        }
    }
    function kill() public {
        if (msg.sender == rakeAddress) {
            selfdestruct(rakeAddress);
        }
    }
}

```

## RQ1_43204b7311ce

SHA-256 `67df2c05a8ac22b17ffb2258da579c0a38594b188796ee073992e582b2c8cdf3`

```solidity
pragma solidity 0.4.25;
contract IAccessPolicy {
    function allowed(
        address subject,
        bytes32 role,
        address object,
        bytes4 verb
    )
        public
        returns (bool);
}
contract IAccessControlled {
    event LogAccessPolicyChanged(
        address controller,
        IAccessPolicy oldPolicy,
        IAccessPolicy newPolicy
    );
    function setAccessPolicy(IAccessPolicy newPolicy, address newAccessController)
        public;
    function accessPolicy()
        public
        constant
        returns (IAccessPolicy);
}
contract StandardRoles {
    bytes32 internal constant ROLE_ACCESS_CONTROLLER = 0xac42f8beb17975ed062dcb80c63e6d203ef1c2c335ced149dc5664cc671cb7da;
}
contract AccessControlled is IAccessControlled, StandardRoles {
    IAccessPolicy private _accessPolicy;
    modifier only(bytes32 role) {
        require(_accessPolicy.allowed(msg.sender, role, this, msg.sig));
        _;
    }
    constructor(IAccessPolicy policy) internal {
        require(address(policy) != 0x0);
        _accessPolicy = policy;
    }
    function setAccessPolicy(IAccessPolicy newPolicy, address newAccessController)
        public
        only(ROLE_ACCESS_CONTROLLER)
    {
        require(newPolicy.allowed(newAccessController, ROLE_ACCESS_CONTROLLER, this, msg.sig));
        IAccessPolicy oldPolicy = _accessPolicy;
        _accessPolicy = newPolicy;
        emit LogAccessPolicyChanged(msg.sender, oldPolicy, newPolicy);
    }
    function accessPolicy()
        public
        constant
        returns (IAccessPolicy)
    {
        return _accessPolicy;
    }
}
contract AccessRoles {
    bytes32 internal constant ROLE_NEUMARK_ISSUER = 0x921c3afa1f1fff707a785f953a1e197bd28c9c50e300424e015953cbf120c06c;
    bytes32 internal constant ROLE_NEUMARK_BURNER = 0x19ce331285f41739cd3362a3ec176edffe014311c0f8075834fdd19d6718e69f;
    bytes32 internal constant ROLE_SNAPSHOT_CREATOR = 0x08c1785afc57f933523bc52583a72ce9e19b2241354e04dd86f41f887e3d8174;
    bytes32 internal constant ROLE_TRANSFER_ADMIN = 0xb6527e944caca3d151b1f94e49ac5e223142694860743e66164720e034ec9b19;
    bytes32 internal constant ROLE_RECLAIMER = 0x0542bbd0c672578966dcc525b30aa16723bb042675554ac5b0362f86b6e97dc5;
    bytes32 internal constant ROLE_PLATFORM_OPERATOR_REPRESENTATIVE = 0xb2b321377653f655206f71514ff9f150d0822d062a5abcf220d549e1da7999f0;
    bytes32 internal constant ROLE_EURT_DEPOSIT_MANAGER = 0x7c8ecdcba80ce87848d16ad77ef57cc196c208fc95c5638e4a48c681a34d4fe7;
    bytes32 internal constant ROLE_IDENTITY_MANAGER = 0x32964e6bc50f2aaab2094a1d311be8bda920fc4fb32b2fb054917bdb153a9e9e;
    bytes32 internal constant ROLE_EURT_LEGAL_MANAGER = 0x4eb6b5806954a48eb5659c9e3982d5e75bfb2913f55199877d877f157bcc5a9b;
    bytes32 internal constant ROLE_UNIVERSE_MANAGER = 0xe8d8f8f9ea4b19a5a4368dbdace17ad71a69aadeb6250e54c7b4c7b446301738;
    bytes32 internal constant ROLE_GAS_EXCHANGE = 0x9fe43636e0675246c99e96d7abf9f858f518b9442c35166d87f0934abef8a969;
    bytes32 internal constant ROLE_TOKEN_RATE_ORACLE = 0xa80c3a0c8a5324136e4c806a778583a2a980f378bdd382921b8d28dcfe965585;
}
contract IEthereumForkArbiter {
    event LogForkAnnounced(
        string name,
        string url,
        uint256 blockNumber
    );
    event LogForkSigned(
        uint256 blockNumber,
        bytes32 blockHash
    );
    function nextForkName()
        public
        constant
        returns (string);
    function nextForkUrl()
        public
        constant
        returns (string);
    function nextForkBlockNumber()
        public
        constant
        returns (uint256);
    function lastSignedBlockNumber()
        public
        constant
        returns (uint256);
    function lastSignedBlockHash()
        public
        constant
        returns (bytes32);
    function lastSignedTimestamp()
        public
        constant
        returns (uint256);
}
contract IAgreement {
    event LogAgreementAccepted(
        address indexed accepter
    );
    event LogAgreementAmended(
        address contractLegalRepresentative,
        string agreementUri
    );
    function amendAgreement(string agreementUri) public;
    function currentAgreement()
        public
        constant
        returns
        (
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        );
    function pastAgreement(uint256 amendmentIndex)
        public
        constant
        returns
        (
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        );
    function agreementSignedAtBlock(address signatory)
        public
        constant
        returns (uint256 blockNo);
    function amendmentsCount()
        public
        constant
        returns (uint256);
}
contract Agreement is
    IAgreement,
    AccessControlled,
    AccessRoles
{
    struct SignedAgreement {
        address contractLegalRepresentative;
        uint256 signedBlockTimestamp;
        string agreementUri;
    }
    IEthereumForkArbiter private ETHEREUM_FORK_ARBITER;
    SignedAgreement[] private _amendments;
    mapping(address => uint256) private _signatories;
    modifier acceptAgreement(address accepter) {
        acceptAgreementInternal(accepter);
        _;
    }
    modifier onlyLegalRepresentative(address legalRepresentative) {
        require(mCanAmend(legalRepresentative));
        _;
    }
    constructor(IAccessPolicy accessPolicy, IEthereumForkArbiter forkArbiter)
        AccessControlled(accessPolicy)
        internal
    {
        require(forkArbiter != IEthereumForkArbiter(0x0));
        ETHEREUM_FORK_ARBITER = forkArbiter;
    }
    function amendAgreement(string agreementUri)
        public
        onlyLegalRepresentative(msg.sender)
    {
        SignedAgreement memory amendment = SignedAgreement({
            contractLegalRepresentative: msg.sender,
            signedBlockTimestamp: block.timestamp,
            agreementUri: agreementUri
        });
        _amendments.push(amendment);
        emit LogAgreementAmended(msg.sender, agreementUri);
    }
    function ethereumForkArbiter()
        public
        constant
        returns (IEthereumForkArbiter)
    {
        return ETHEREUM_FORK_ARBITER;
    }
    function currentAgreement()
        public
        constant
        returns
        (
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        )
    {
        require(_amendments.length > 0);
        uint256 last = _amendments.length - 1;
        SignedAgreement storage amendment = _amendments[last];
        return (
            amendment.contractLegalRepresentative,
            amendment.signedBlockTimestamp,
            amendment.agreementUri,
            last
        );
    }
    function pastAgreement(uint256 amendmentIndex)
        public
        constant
        returns
        (
            address contractLegalRepresentative,
            uint256 signedBlockTimestamp,
            string agreementUri,
            uint256 index
        )
    {
        SignedAgreement storage amendment = _amendments[amendmentIndex];
        return (
            amendment.contractLegalRepresentative,
            amendment.signedBlockTimestamp,
            amendment.agreementUri,
            amendmentIndex
        );
    }
    function agreementSignedAtBlock(address signatory)
        public
        constant
        returns (uint256 blockNo)
    {
        return _signatories[signatory];
    }
    function amendmentsCount()
        public
        constant
        returns (uint256)
    {
        return _amendments.length;
    }
    function acceptAgreementInternal(address accepter)
        internal
    {
        if(_signatories[accepter] == 0) {
            require(_amendments.length > 0);
            _signatories[accepter] = block.number;
            emit LogAgreementAccepted(accepter);
        }
    }
    function mCanAmend(address legalRepresentative)
        internal
        returns (bool)
    {
        return accessPolicy().allowed(legalRepresentative, ROLE_PLATFORM_OPERATOR_REPRESENTATIVE, this, msg.sig);
    }
}
contract ITokenSnapshots {
    function totalSupplyAt(uint256 snapshotId)
        public
        constant
        returns(uint256);
    function balanceOfAt(address owner, uint256 snapshotId)
        public
        constant
        returns (uint256);
    function currentSnapshotId()
        public
        constant
        returns (uint256);
}
contract IClonedTokenParent is ITokenSnapshots {
    function parentToken()
        public
        constant
        returns(IClonedTokenParent parent);
    function parentSnapshotId()
        public
        constant
        returns(uint256 snapshotId);
}
contract IBasicToken {
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 amount
    );
    function totalSupply()
        public
        constant
        returns (uint256);
    function balanceOf(address owner)
        public
        constant
        returns (uint256 balance);
    function transfer(address to, uint256 amount)
        public
        returns (bool success);
}
contract IERC20Allowance {
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 amount
    );
    function allowance(address owner, address spender)
        public
        constant
        returns (uint256 remaining);
    function approve(address spender, uint256 amount)
        public
        returns (bool success);
    function transferFrom(address from, address to, uint256 amount)
        public
        returns (bool success);
}
contract IERC20Token is IBasicToken, IERC20Allowance {
}
contract ITokenMetadata {
    function symbol()
        public
        constant
        returns (string);
    function name()
        public
        constant
        returns (string);
    function decimals()
        public
        constant
        returns (uint8);
}
contract IERC223Token is IERC20Token, ITokenMetadata {
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool);
}
contract IERC677Allowance is IERC20Allowance {
    function approveAndCall(address spender, uint256 amount, bytes extraData)
        public
        returns (bool success);
}
contract IERC677Token is IERC20Token, IERC677Allowance {
}
contract ITokenControllerHook {
    event LogChangeTokenController(
        address oldController,
        address newController,
        address by
    );
    function changeTokenController(address newController)
        public;
    function tokenController()
        public
        constant
        returns (address currentController);
}
contract IETOCommitmentStates {
    enum ETOState {
        Setup, 
        Whitelist,
        Public,
        Signing,
        Claim,
        Payout, 
        Refund 
    }
    uint256 constant internal ETO_STATES_COUNT = 7;
}
contract IETOCommitmentObserver is IETOCommitmentStates {
    function commitmentObserver() public constant returns (address);
    function onStateTransition(ETOState oldState, ETOState newState) public;
}
contract IERC223Callback {
    function tokenFallback(address from, uint256 amount, bytes data)
        public;
}
contract ITokenController {
    function onTransfer(address broker, address from, address to, uint256 amount)
        public
        constant
        returns (bool allow);
    function onApprove(address owner, address spender, uint256 amount)
        public
        constant
        returns (bool allow);
    function onGenerateTokens(address sender, address owner, uint256 amount)
        public
        constant
        returns (bool allow);
    function onDestroyTokens(address sender, address owner, uint256 amount)
        public
        constant
        returns (bool allow);
    function onChangeTokenController(address sender, address newController)
        public
        constant
        returns (bool);
    function onAllowance(address owner, address spender)
        public
        constant
        returns (uint256 allowanceOverride);
}
contract IEquityTokenController is
    IAgreement,
    ITokenController,
    IETOCommitmentObserver,
    IERC223Callback
{
    function onChangeNominee(address sender, address oldNominee, address newNominee)
        public
        constant
        returns (bool);
}
contract IEquityToken is
    IAgreement,
    IClonedTokenParent,
    IERC223Token,
    ITokenControllerHook
{
    function tokensPerShare() public constant returns (uint256);
    function sharesTotalSupply() public constant returns (uint256);
    function shareNominalValueEurUlps() public constant returns (uint256);
    function companyLegalRepresentative() public constant returns (address);
    function nominee() public constant returns (address);
    function changeNominee(address newNominee) public;
    function issueTokens(uint256 amount) public;
    function distributeTokens(address to, uint256 amount) public;
    function destroyTokens(uint256 amount) public;
}
contract IContractId {
    function contractId() public pure returns (bytes32 id, uint256 version);
}
contract ShareholderRights is IContractId {
    enum VotingRule {
        NoVotingRights,
        Positive,
        Negative,
        Proportional
    }
    bytes32 private constant EMPTY_STRING_HASH = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
    bool public constant HAS_DRAG_ALONG_RIGHTS = true;
    bool public constant HAS_TAG_ALONG_RIGHTS = true;
    bool public constant HAS_GENERAL_INFORMATION_RIGHTS = true;
    VotingRule public GENERAL_VOTING_RULE;
    VotingRule public TAG_ALONG_VOTING_RULE;
    uint256 public LIQUIDATION_PREFERENCE_MULTIPLIER_FRAC;
    bool public HAS_FOUNDERS_VESTING;
    uint256 public GENERAL_VOTING_DURATION;
    uint256 public RESTRICTED_ACT_VOTING_DURATION;
    uint256 public VOTING_FINALIZATION_DURATION;
    uint256 public TOKENHOLDERS_QUORUM_FRAC = 10**17; 
    uint256 public VOTING_MAJORITY_FRAC = 10**17; 
    string public INVESTMENT_AGREEMENT_TEMPLATE_URL;
    constructor(
        VotingRule generalVotingRule,
        VotingRule tagAlongVotingRule,
        uint256 liquidationPreferenceMultiplierFrac,
        bool hasFoundersVesting,
        uint256 generalVotingDuration,
        uint256 restrictedActVotingDuration,
        uint256 votingFinalizationDuration,
        uint256 tokenholdersQuorumFrac,
        uint256 votingMajorityFrac,
        string investmentAgreementTemplateUrl
    )
        public
    {
        require(uint(generalVotingRule) < 4);
        require(uint(tagAlongVotingRule) < 4);
        require(tokenholdersQuorumFrac < 10**18);
        require(keccak256(abi.encodePacked(investmentAgreementTemplateUrl)) != EMPTY_STRING_HASH);
        GENERAL_VOTING_RULE = generalVotingRule;
        TAG_ALONG_VOTING_RULE = tagAlongVotingRule;
        LIQUIDATION_PREFERENCE_MULTIPLIER_FRAC = liquidationPreferenceMultiplierFrac;
        HAS_FOUNDERS_VESTING = hasFoundersVesting;
        GENERAL_VOTING_DURATION = generalVotingDuration;
        RESTRICTED_ACT_VOTING_DURATION = restrictedActVotingDuration;
        VOTING_FINALIZATION_DURATION = votingFinalizationDuration;
        TOKENHOLDERS_QUORUM_FRAC = tokenholdersQuorumFrac;
        VOTING_MAJORITY_FRAC = votingMajorityFrac;
        INVESTMENT_AGREEMENT_TEMPLATE_URL = investmentAgreementTemplateUrl;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x7f46caed28b4e7a90dc4db9bba18d1565e6c4824f0dc1b96b3b88d730da56e57, 0);
    }
}
contract Math {
    function absDiff(uint256 v1, uint256 v2)
        internal
        pure
        returns(uint256)
    {
        return v1 > v2 ? v1 - v2 : v2 - v1;
    }
    function divRound(uint256 v, uint256 d)
        internal
        pure
        returns(uint256)
    {
        return add(v, d/2) / d;
    }
    function decimalFraction(uint256 amount, uint256 frac)
        internal
        pure
        returns(uint256)
    {
        return proportion(amount, frac, 10**18);
    }
    function proportion(uint256 amount, uint256 part, uint256 total)
        internal
        pure
        returns(uint256)
    {
        return divRound(mul(amount, part), total);
    }
    function mul(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        uint256 c = a * b;
        assert(a == 0 || c / a == b);
        return c;
    }
    function sub(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        assert(b <= a);
        return a - b;
    }
    function add(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
    function min(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        return a < b ? a : b;
    }
    function max(uint256 a, uint256 b)
        internal
        pure
        returns (uint256)
    {
        return a > b ? a : b;
    }
}
contract PlatformTerms is Math, IContractId {
    uint256 public constant PLATFORM_FEE_FRACTION = 3 * 10**16;
    uint256 public constant TOKEN_PARTICIPATION_FEE_FRACTION = 2 * 10**16;
    uint256 public constant PLATFORM_NEUMARK_SHARE = 2; 
    bool public constant IS_ICBM_INVESTOR_WHITELISTED = true;
    uint256 public constant MIN_TICKET_EUR_ULPS = 100 * 10**18;
    uint256 public constant DATE_TO_WHITELIST_MIN_DURATION = 5 days;
    uint256 public constant TOKEN_RATE_EXPIRES_AFTER = 4 hours;
    uint256 public constant MIN_WHITELIST_DURATION = 0 days;
    uint256 public constant MAX_WHITELIST_DURATION = 30 days;
    uint256 public constant MIN_PUBLIC_DURATION = 0 days;
    uint256 public constant MAX_PUBLIC_DURATION = 60 days;
    uint256 public constant MIN_OFFER_DURATION = 1 days;
    uint256 public constant MAX_OFFER_DURATION = 90 days;
    uint256 public constant MIN_SIGNING_DURATION = 14 days;
    uint256 public constant MAX_SIGNING_DURATION = 60 days;
    uint256 public constant MIN_CLAIM_DURATION = 7 days;
    uint256 public constant MAX_CLAIM_DURATION = 30 days;
    function calculateNeumarkDistribution(uint256 rewardNmk)
        public
        pure
        returns (uint256 platformNmk, uint256 investorNmk)
    {
        platformNmk = rewardNmk / PLATFORM_NEUMARK_SHARE;
        return (platformNmk, rewardNmk - platformNmk);
    }
    function calculatePlatformTokenFee(uint256 tokenAmount)
        public
        pure
        returns (uint256)
    {
        return proportion(tokenAmount, TOKEN_PARTICIPATION_FEE_FRACTION, 10**18);
    }
    function calculatePlatformFee(uint256 amount)
        public
        pure
        returns (uint256)
    {
        return decimalFraction(amount, PLATFORM_FEE_FRACTION);
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x95482babc4e32de6c4dc3910ee7ae62c8e427efde6bc4e9ce0d6d93e24c39323, 0);
    }
}
contract IdentityRecord {
    struct IdentityClaims {
        bool isVerified; 
        bool isSophisticatedInvestor; 
        bool hasBankAccount; 
        bool accountFrozen; 
    }
    function deserializeClaims(bytes32 data) internal pure returns (IdentityClaims memory claims) {
        assembly {
            mstore(claims, and(data, 0x1))
            mstore(add(claims, 0x20), div(and(data, 0x2), 0x2))
            mstore(add(claims, 0x40), div(and(data, 0x4), 0x4))
            mstore(add(claims, 0x60), div(and(data, 0x8), 0x8))
        }
    }
}
contract IIdentityRegistry {
    event LogSetClaims(
        address indexed identity,
        bytes32 oldClaims,
        bytes32 newClaims
    );
    function getClaims(address identity) public constant returns (bytes32);
    function setClaims(address identity, bytes32 oldClaims, bytes32 newClaims) public;
}
contract KnownInterfaces {
    bytes4 internal constant KNOWN_INTERFACE_NEUMARK = 0xeb41a1bd;
    bytes4 internal constant KNOWN_INTERFACE_ETHER_TOKEN = 0x8cf73cf1;
    bytes4 internal constant KNOWN_INTERFACE_EURO_TOKEN = 0x83c3790b;
    bytes4 internal constant KNOWN_INTERFACE_IDENTITY_REGISTRY = 0x0a72e073;
    bytes4 internal constant KNOWN_INTERFACE_TOKEN_EXCHANGE_RATE_ORACLE = 0xc6e5349e;
    bytes4 internal constant KNOWN_INTERFACE_FEE_DISBURSAL = 0xf4c848e8;
    bytes4 internal constant KNOWN_INTERFACE_PLATFORM_PORTFOLIO = 0xaa1590d0;
    bytes4 internal constant KNOWN_INTERFACE_TOKEN_EXCHANGE = 0xddd7a521;
    bytes4 internal constant KNOWN_INTERFACE_GAS_EXCHANGE = 0x89dbc6de;
    bytes4 internal constant KNOWN_INTERFACE_ACCESS_POLICY = 0xb05049d9;
    bytes4 internal constant KNOWN_INTERFACE_EURO_LOCK = 0x2347a19e;
    bytes4 internal constant KNOWN_INTERFACE_ETHER_LOCK = 0x978a6823;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_EURO_LOCK = 0x36021e14;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_ETHER_LOCK = 0x0b58f006;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_ETHER_TOKEN = 0xae8b50b9;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_EURO_TOKEN = 0xc2c6cd72;
    bytes4 internal constant KNOWN_INTERFACE_ICBM_COMMITMENT = 0x7f2795ef;
    bytes4 internal constant KNOWN_INTERFACE_FORK_ARBITER = 0x2fe7778c;
    bytes4 internal constant KNOWN_INTERFACE_PLATFORM_TERMS = 0x75ecd7f8;
    bytes4 internal constant KNOWN_INTERFACE_UNIVERSE = 0xbf202454;
    bytes4 internal constant KNOWN_INTERFACE_COMMITMENT = 0xfa0e0c60;
    bytes4 internal constant KNOWN_INTERFACE_EQUITY_TOKEN_CONTROLLER = 0xfa30b2f1;
    bytes4 internal constant KNOWN_INTERFACE_EQUITY_TOKEN = 0xab9885bb;
}
contract IsContract {
    function isContract(address addr)
        internal
        constant
        returns (bool)
    {
        uint256 size;
        assembly { size := extcodesize(addr) }
        return size > 0;
    }
}
contract NeumarkIssuanceCurve {
    uint256 private constant NEUMARK_CAP = 1500000000000000000000000000;
    uint256 private constant INITIAL_REWARD_FRACTION = 6500000000000000000;
    uint256 private constant ISSUANCE_LIMIT_EUR_ULPS = 8300000000000000000000000000;
    uint256 private constant LINEAR_APPROX_LIMIT_EUR_ULPS = 2100000000000000000000000000;
    uint256 private constant NEUMARKS_AT_LINEAR_LIMIT_ULPS = 1499832501287264827896539871;
    uint256 private constant TOT_LINEAR_NEUMARKS_ULPS = NEUMARK_CAP - NEUMARKS_AT_LINEAR_LIMIT_ULPS;
    uint256 private constant TOT_LINEAR_EUR_ULPS = ISSUANCE_LIMIT_EUR_ULPS - LINEAR_APPROX_LIMIT_EUR_ULPS;
    function incremental(uint256 totalEuroUlps, uint256 euroUlps)
        public
        pure
        returns (uint256 neumarkUlps)
    {
        require(totalEuroUlps + euroUlps >= totalEuroUlps);
        uint256 from = cumulative(totalEuroUlps);
        uint256 to = cumulative(totalEuroUlps + euroUlps);
        assert(to >= from);
        return to - from;
    }
    function incrementalInverse(uint256 totalEuroUlps, uint256 burnNeumarkUlps)
        public
        pure
        returns (uint256 euroUlps)
    {
        uint256 totalNeumarkUlps = cumulative(totalEuroUlps);
        require(totalNeumarkUlps >= burnNeumarkUlps);
        uint256 fromNmk = totalNeumarkUlps - burnNeumarkUlps;
        uint newTotalEuroUlps = cumulativeInverse(fromNmk, 0, totalEuroUlps);
        assert(totalEuroUlps >= newTotalEuroUlps);
        return totalEuroUlps - newTotalEuroUlps;
    }
    function incrementalInverse(uint256 totalEuroUlps, uint256 burnNeumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        public
        pure
        returns (uint256 euroUlps)
    {
        uint256 totalNeumarkUlps = cumulative(totalEuroUlps);
        require(totalNeumarkUlps >= burnNeumarkUlps);
        uint256 fromNmk = totalNeumarkUlps - burnNeumarkUlps;
        uint newTotalEuroUlps = cumulativeInverse(fromNmk, minEurUlps, maxEurUlps);
        assert(totalEuroUlps >= newTotalEuroUlps);
        return totalEuroUlps - newTotalEuroUlps;
    }
    function cumulative(uint256 euroUlps)
        public
        pure
        returns(uint256 neumarkUlps)
    {
        if (euroUlps >= ISSUANCE_LIMIT_EUR_ULPS) {
            return NEUMARK_CAP;
        }
        if (euroUlps >= LINEAR_APPROX_LIMIT_EUR_ULPS) {
            return NEUMARKS_AT_LINEAR_LIMIT_ULPS + (TOT_LINEAR_NEUMARKS_ULPS * (euroUlps - LINEAR_APPROX_LIMIT_EUR_ULPS)) / TOT_LINEAR_EUR_ULPS;
        }
        uint256 d = 230769230769230769230769231; 
        uint256 term = NEUMARK_CAP;
        uint256 sum = 0;
        uint256 denom = d;
        do assembly {
            term  := div(mul(term, euroUlps), denom)
            sum   := add(sum, term)
            denom := add(denom, d)
            term  := div(mul(term, euroUlps), denom)
            sum   := sub(sum, term)
            denom := add(denom, d)
        } while (term != 0);
        return sum;
    }
    function cumulativeInverse(uint256 neumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        public
        pure
        returns (uint256 euroUlps)
    {
        require(maxEurUlps >= minEurUlps);
        require(cumulative(minEurUlps) <= neumarkUlps);
        require(cumulative(maxEurUlps) >= neumarkUlps);
        uint256 min = minEurUlps;
        uint256 max = maxEurUlps;
        while (max > min) {
            uint256 mid = (max + min) / 2;
            uint256 val = cumulative(mid);
            if (val < neumarkUlps) {
                min = mid + 1;
            } else {
                max = mid;
            }
        }
        return max;
    }
    function neumarkCap()
        public
        pure
        returns (uint256)
    {
        return NEUMARK_CAP;
    }
    function initialRewardFraction()
        public
        pure
        returns (uint256)
    {
        return INITIAL_REWARD_FRACTION;
    }
}
contract Reclaimable is AccessControlled, AccessRoles {
    IBasicToken constant internal RECLAIM_ETHER = IBasicToken(0x0);
    function reclaim(IBasicToken token)
        public
        only(ROLE_RECLAIMER)
    {
        address reclaimer = msg.sender;
        if(token == RECLAIM_ETHER) {
            reclaimer.transfer(address(this).balance);
        } else {
            uint256 balance = token.balanceOf(this);
            require(token.transfer(reclaimer, balance));
        }
    }
}
contract ISnapshotable {
    event LogSnapshotCreated(uint256 snapshotId);
    function createSnapshot()
        public
        returns (uint256);
    function currentSnapshotId()
        public
        constant
        returns (uint256);
}
contract MSnapshotPolicy {
    function mAdvanceSnapshotId()
        internal
        returns (uint256);
    function mCurrentSnapshotId()
        internal
        constant
        returns (uint256);
}
contract Daily is MSnapshotPolicy {
    uint256 private MAX_TIMESTAMP = 3938453320844195178974243141571391;
    constructor(uint256 start) internal {
        if (start > 0) {
            uint256 base = dayBase(uint128(block.timestamp));
            require(start >= base);
            require(start < base + 2**128);
        }
    }
    function snapshotAt(uint256 timestamp)
        public
        constant
        returns (uint256)
    {
        require(timestamp < MAX_TIMESTAMP);
        return dayBase(uint128(timestamp));
    }
    function mAdvanceSnapshotId()
        internal
        returns (uint256)
    {
        return mCurrentSnapshotId();
    }
    function mCurrentSnapshotId()
        internal
        constant
        returns (uint256)
    {
        return dayBase(uint128(block.timestamp));
    }
    function dayBase(uint128 timestamp)
        internal
        pure
        returns (uint256)
    {
        return 2**128 * (uint256(timestamp) / 1 days);
    }
}
contract DailyAndSnapshotable is
    Daily,
    ISnapshotable
{
    uint256 private _currentSnapshotId;
    constructor(uint256 start)
        internal
        Daily(start)
    {
        if (start > 0) {
            _currentSnapshotId = start;
        }
    }
    function createSnapshot()
        public
        returns (uint256)
    {
        uint256 base = dayBase(uint128(block.timestamp));
        if (base > _currentSnapshotId) {
            _currentSnapshotId = base;
        } else {
            _currentSnapshotId += 1;
        }
        emit LogSnapshotCreated(_currentSnapshotId);
        return _currentSnapshotId;
    }
    function mAdvanceSnapshotId()
        internal
        returns (uint256)
    {
        uint256 base = dayBase(uint128(block.timestamp));
        if (base > _currentSnapshotId) {
            _currentSnapshotId = base;
            emit LogSnapshotCreated(base);
        }
        return _currentSnapshotId;
    }
    function mCurrentSnapshotId()
        internal
        constant
        returns (uint256)
    {
        uint256 base = dayBase(uint128(block.timestamp));
        return base > _currentSnapshotId ? base : _currentSnapshotId;
    }
}
contract TokenMetadata is ITokenMetadata {
    string private NAME;
    string private SYMBOL;
    uint8 private DECIMALS;
    string private VERSION;
    constructor(
        string tokenName,
        uint8 decimalUnits,
        string tokenSymbol,
        string version
    )
        public
    {
        NAME = tokenName;                                 
        SYMBOL = tokenSymbol;                             
        DECIMALS = decimalUnits;                          
        VERSION = version;
    }
    function name()
        public
        constant
        returns (string)
    {
        return NAME;
    }
    function symbol()
        public
        constant
        returns (string)
    {
        return SYMBOL;
    }
    function decimals()
        public
        constant
        returns (uint8)
    {
        return DECIMALS;
    }
    function version()
        public
        constant
        returns (string)
    {
        return VERSION;
    }
}
contract MTokenAllowanceController {
    function mOnApprove(
        address owner,
        address spender,
        uint256 amount
    )
        internal
        returns (bool allow);
    function mAllowanceOverride(
        address owner,
        address spender
    )
        internal
        constant
        returns (uint256 allowance);
}
contract MTokenTransferController {
    function mOnTransfer(
        address from,
        address to,
        uint256 amount
    )
        internal
        returns (bool allow);
}
contract MTokenController is MTokenTransferController, MTokenAllowanceController {
}
contract MTokenTransfer {
    function mTransfer(
        address from,
        address to,
        uint256 amount
    )
        internal;
}
contract IERC677Callback {
    function receiveApproval(
        address from,
        uint256 amount,
        address token, 
        bytes data
    )
        public
        returns (bool success);
}
contract TokenAllowance is
    MTokenTransfer,
    MTokenAllowanceController,
    IERC20Allowance,
    IERC677Token
{
    mapping (address => mapping (address => uint256)) private _allowed;
    constructor()
        internal
    {
    }
    function allowance(address owner, address spender)
        public
        constant
        returns (uint256 remaining)
    {
        uint256 override = mAllowanceOverride(owner, spender);
        if (override > 0) {
            return override;
        }
        return _allowed[owner][spender];
    }
    function approve(address spender, uint256 amount)
        public
        returns (bool success)
    {
        require(mOnApprove(msg.sender, spender, amount));
        require((amount == 0 || _allowed[msg.sender][spender] == 0) && mAllowanceOverride(msg.sender, spender) == 0);
        _allowed[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }
    function transferFrom(address from, address to, uint256 amount)
        public
        returns (bool success)
    {
        uint256 allowed = mAllowanceOverride(from, msg.sender);
        if (allowed == 0) {
            allowed = _allowed[from][msg.sender];
            _allowed[from][msg.sender] -= amount;
        }
        require(allowed >= amount);
        mTransfer(from, to, amount);
        return true;
    }
    function approveAndCall(
        address spender,
        uint256 amount,
        bytes extraData
    )
        public
        returns (bool success)
    {
        require(approve(spender, amount));
        success = IERC677Callback(spender).receiveApproval(
            msg.sender,
            amount,
            this,
            extraData
        );
        require(success);
        return true;
    }
    function mAllowanceOverride(
        address ,
        address 
    )
        internal
        constant
        returns (uint256)
    {
        return 0;
    }
}
contract Snapshot is MSnapshotPolicy {
    struct Values {
        uint256 snapshotId;
        uint256 value;
    }
    function hasValue(
        Values[] storage values
    )
        internal
        constant
        returns (bool)
    {
        return values.length > 0;
    }
    function hasValueAt(
        Values[] storage values,
        uint256 snapshotId
    )
        internal
        constant
        returns (bool)
    {
        require(snapshotId <= mCurrentSnapshotId());
        return values.length > 0 && values[0].snapshotId <= snapshotId;
    }
    function getValue(
        Values[] storage values,
        uint256 defaultValue
    )
        internal
        constant
        returns (uint256)
    {
        if (values.length == 0) {
            return defaultValue;
        } else {
            uint256 last = values.length - 1;
            return values[last].value;
        }
    }
    function getValueAt(
        Values[] storage values,
        uint256 snapshotId,
        uint256 defaultValue
    )
        internal
        constant
        returns (uint256)
    {
        require(snapshotId <= mCurrentSnapshotId());
        if (values.length == 0) {
            return defaultValue;
        }
        uint256 last = values.length - 1;
        uint256 lastSnapshot = values[last].snapshotId;
        if (snapshotId >= lastSnapshot) {
            return values[last].value;
        }
        uint256 firstSnapshot = values[0].snapshotId;
        if (snapshotId < firstSnapshot) {
            return defaultValue;
        }
        uint256 min = 0;
        uint256 max = last;
        while (max > min) {
            uint256 mid = (max + min + 1) / 2;
            if (values[mid].snapshotId <= snapshotId) {
                min = mid;
            } else {
                max = mid - 1;
            }
        }
        return values[min].value;
    }
    function setValue(
        Values[] storage values,
        uint256 value
    )
        internal
    {
        uint256 currentSnapshotId = mAdvanceSnapshotId();
        bool empty = values.length == 0;
        if (empty) {
            values.push(
                Values({
                    snapshotId: currentSnapshotId,
                    value: value
                })
            );
            return;
        }
        uint256 last = values.length - 1;
        bool hasNewSnapshot = values[last].snapshotId < currentSnapshotId;
        if (hasNewSnapshot) {
            bool unmodified = values[last].value == value;
            if (unmodified) {
                return;
            }
            values.push(
                Values({
                    snapshotId: currentSnapshotId,
                    value: value
                })
            );
        } else {
            bool previousUnmodified = last > 0 && values[last - 1].value == value;
            if (previousUnmodified) {
                delete values[last];
                values.length--;
                return;
            }
            values[last].value = value;
        }
    }
}
contract BasicSnapshotToken is
    MTokenTransfer,
    MTokenTransferController,
    IClonedTokenParent,
    IBasicToken,
    Snapshot
{
    IClonedTokenParent private PARENT_TOKEN;
    uint256 private PARENT_SNAPSHOT_ID;
    mapping (address => Values[]) internal _balances;
    Values[] internal _totalSupplyValues;
    constructor(
        IClonedTokenParent parentToken,
        uint256 parentSnapshotId
    )
        Snapshot()
        internal
    {
        PARENT_TOKEN = parentToken;
        if (parentToken == address(0)) {
            require(parentSnapshotId == 0);
        } else {
            if (parentSnapshotId == 0) {
                require(parentToken.currentSnapshotId() > 0);
                PARENT_SNAPSHOT_ID = parentToken.currentSnapshotId() - 1;
            } else {
                PARENT_SNAPSHOT_ID = parentSnapshotId;
            }
        }
    }
    function totalSupply()
        public
        constant
        returns (uint256)
    {
        return totalSupplyAtInternal(mCurrentSnapshotId());
    }
    function balanceOf(address owner)
        public
        constant
        returns (uint256 balance)
    {
        return balanceOfAtInternal(owner, mCurrentSnapshotId());
    }
    function transfer(address to, uint256 amount)
        public
        returns (bool success)
    {
        mTransfer(msg.sender, to, amount);
        return true;
    }
    function totalSupplyAt(uint256 snapshotId)
        public
        constant
        returns(uint256)
    {
        return totalSupplyAtInternal(snapshotId);
    }
    function balanceOfAt(address owner, uint256 snapshotId)
        public
        constant
        returns (uint256)
    {
        return balanceOfAtInternal(owner, snapshotId);
    }
    function currentSnapshotId()
        public
        constant
        returns (uint256)
    {
        return mCurrentSnapshotId();
    }
    function parentToken()
        public
        constant
        returns(IClonedTokenParent parent)
    {
        return PARENT_TOKEN;
    }
    function parentSnapshotId()
        public
        constant
        returns(uint256 snapshotId)
    {
        return PARENT_SNAPSHOT_ID;
    }
    function allBalancesOf(address owner)
        external
        constant
        returns (uint256[2][])
    {
        Values[] storage values = _balances[owner];
        uint256[2][] memory balances = new uint256[2][](values.length);
        for(uint256 ii = 0; ii < values.length; ++ii) {
            balances[ii] = [values[ii].snapshotId, values[ii].value];
        }
        return balances;
    }
    function totalSupplyAtInternal(uint256 snapshotId)
        internal
        constant
        returns(uint256)
    {
        Values[] storage values = _totalSupplyValues;
        if (hasValueAt(values, snapshotId)) {
            return getValueAt(values, snapshotId, 0);
        }
        if (address(PARENT_TOKEN) != 0) {
            uint256 earlierSnapshotId = PARENT_SNAPSHOT_ID > snapshotId ? snapshotId : PARENT_SNAPSHOT_ID;
            return PARENT_TOKEN.totalSupplyAt(earlierSnapshotId);
        }
        return 0;
    }
    function balanceOfAtInternal(address owner, uint256 snapshotId)
        internal
        constant
        returns (uint256)
    {
        Values[] storage values = _balances[owner];
        if (hasValueAt(values, snapshotId)) {
            return getValueAt(values, snapshotId, 0);
        }
        if (PARENT_TOKEN != address(0)) {
            uint256 earlierSnapshotId = PARENT_SNAPSHOT_ID > snapshotId ? snapshotId : PARENT_SNAPSHOT_ID;
            return PARENT_TOKEN.balanceOfAt(owner, earlierSnapshotId);
        }
        return 0;
    }
    function mTransfer(
        address from,
        address to,
        uint256 amount
    )
        internal
    {
        require(to != address(0));
        require(parentToken() == address(0) || parentSnapshotId() < parentToken().currentSnapshotId());
        require(mOnTransfer(from, to, amount));
        uint256 previousBalanceFrom = balanceOf(from);
        require(previousBalanceFrom >= amount);
        uint256 newBalanceFrom = previousBalanceFrom - amount;
        setValue(_balances[from], newBalanceFrom);
        uint256 previousBalanceTo = balanceOf(to);
        uint256 newBalanceTo = previousBalanceTo + amount;
        assert(newBalanceTo >= previousBalanceTo); 
        setValue(_balances[to], newBalanceTo);
        emit Transfer(from, to, amount);
    }
}
contract MTokenMint {
    function mGenerateTokens(address owner, uint256 amount)
        internal;
    function mDestroyTokens(address owner, uint256 amount)
        internal;
}
contract MintableSnapshotToken is
    BasicSnapshotToken,
    MTokenMint
{
    constructor(
        IClonedTokenParent parentToken,
        uint256 parentSnapshotId
    )
        BasicSnapshotToken(parentToken, parentSnapshotId)
        internal
    {}
    function mGenerateTokens(address owner, uint256 amount)
        internal
    {
        require(owner != address(0));
        require(parentToken() == address(0) || parentSnapshotId() < parentToken().currentSnapshotId());
        uint256 curTotalSupply = totalSupply();
        uint256 newTotalSupply = curTotalSupply + amount;
        require(newTotalSupply >= curTotalSupply); 
        uint256 previousBalanceTo = balanceOf(owner);
        uint256 newBalanceTo = previousBalanceTo + amount;
        assert(newBalanceTo >= previousBalanceTo); 
        setValue(_totalSupplyValues, newTotalSupply);
        setValue(_balances[owner], newBalanceTo);
        emit Transfer(0, owner, amount);
    }
    function mDestroyTokens(address owner, uint256 amount)
        internal
    {
        require(parentToken() == address(0) || parentSnapshotId() < parentToken().currentSnapshotId());
        uint256 curTotalSupply = totalSupply();
        require(curTotalSupply >= amount);
        uint256 previousBalanceFrom = balanceOf(owner);
        require(previousBalanceFrom >= amount);
        uint256 newTotalSupply = curTotalSupply - amount;
        uint256 newBalanceFrom = previousBalanceFrom - amount;
        setValue(_totalSupplyValues, newTotalSupply);
        setValue(_balances[owner], newBalanceFrom);
        emit Transfer(owner, 0, amount);
    }
}
contract StandardSnapshotToken is
    MintableSnapshotToken,
    TokenAllowance
{
    constructor(
        IClonedTokenParent parentToken,
        uint256 parentSnapshotId
    )
        MintableSnapshotToken(parentToken, parentSnapshotId)
        TokenAllowance()
        internal
    {}
}
contract IERC223LegacyCallback {
    function onTokenTransfer(address from, uint256 amount, bytes data)
        public;
}
contract Neumark is
    AccessControlled,
    AccessRoles,
    Agreement,
    DailyAndSnapshotable,
    StandardSnapshotToken,
    TokenMetadata,
    IERC223Token,
    NeumarkIssuanceCurve,
    Reclaimable,
    IsContract
{
    string private constant TOKEN_NAME = "Neumark";
    uint8  private constant TOKEN_DECIMALS = 18;
    string private constant TOKEN_SYMBOL = "NEU";
    string private constant VERSION = "NMK_1.0";
    bool private _transferEnabled = false;
    uint256 private _totalEurUlps;
    event LogNeumarksIssued(
        address indexed owner,
        uint256 euroUlps,
        uint256 neumarkUlps
    );
    event LogNeumarksBurned(
        address indexed owner,
        uint256 euroUlps,
        uint256 neumarkUlps
    );
    constructor(
        IAccessPolicy accessPolicy,
        IEthereumForkArbiter forkArbiter
    )
        AccessRoles()
        Agreement(accessPolicy, forkArbiter)
        StandardSnapshotToken(
            IClonedTokenParent(0x0),
            0
        )
        TokenMetadata(
            TOKEN_NAME,
            TOKEN_DECIMALS,
            TOKEN_SYMBOL,
            VERSION
        )
        DailyAndSnapshotable(0)
        NeumarkIssuanceCurve()
        Reclaimable()
        public
    {}
    function issueForEuro(uint256 euroUlps)
        public
        only(ROLE_NEUMARK_ISSUER)
        acceptAgreement(msg.sender)
        returns (uint256)
    {
        require(_totalEurUlps + euroUlps >= _totalEurUlps);
        uint256 neumarkUlps = incremental(_totalEurUlps, euroUlps);
        _totalEurUlps += euroUlps;
        mGenerateTokens(msg.sender, neumarkUlps);
        emit LogNeumarksIssued(msg.sender, euroUlps, neumarkUlps);
        return neumarkUlps;
    }
    function distribute(address to, uint256 neumarkUlps)
        public
        only(ROLE_NEUMARK_ISSUER)
        acceptAgreement(to)
    {
        mTransfer(msg.sender, to, neumarkUlps);
    }
    function burn(uint256 neumarkUlps)
        public
        only(ROLE_NEUMARK_BURNER)
    {
        burnPrivate(neumarkUlps, 0, _totalEurUlps);
    }
    function burn(uint256 neumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        public
        only(ROLE_NEUMARK_BURNER)
    {
        burnPrivate(neumarkUlps, minEurUlps, maxEurUlps);
    }
    function enableTransfer(bool enabled)
        public
        only(ROLE_TRANSFER_ADMIN)
    {
        _transferEnabled = enabled;
    }
    function createSnapshot()
        public
        only(ROLE_SNAPSHOT_CREATOR)
        returns (uint256)
    {
        return DailyAndSnapshotable.createSnapshot();
    }
    function transferEnabled()
        public
        constant
        returns (bool)
    {
        return _transferEnabled;
    }
    function totalEuroUlps()
        public
        constant
        returns (uint256)
    {
        return _totalEurUlps;
    }
    function incremental(uint256 euroUlps)
        public
        constant
        returns (uint256 neumarkUlps)
    {
        return incremental(_totalEurUlps, euroUlps);
    }
    function transfer(address to, uint256 amount, bytes data)
        public
        returns (bool)
    {
        BasicSnapshotToken.mTransfer(msg.sender, to, amount);
        if (isContract(to)) {
            IERC223LegacyCallback(to).onTokenTransfer(msg.sender, amount, data);
        }
        return true;
    }
    function mOnTransfer(
        address from,
        address, 
        uint256 
    )
        internal
        acceptAgreement(from)
        returns (bool allow)
    {
        return _transferEnabled || accessPolicy().allowed(msg.sender, ROLE_NEUMARK_ISSUER, this, msg.sig);
    }
    function mOnApprove(
        address owner,
        address, 
        uint256 
    )
        internal
        acceptAgreement(owner)
        returns (bool allow)
    {
        return true;
    }
    function burnPrivate(uint256 burnNeumarkUlps, uint256 minEurUlps, uint256 maxEurUlps)
        private
    {
        uint256 prevEuroUlps = _totalEurUlps;
        mDestroyTokens(msg.sender, burnNeumarkUlps);
        _totalEurUlps = cumulativeInverse(totalSupply(), minEurUlps, maxEurUlps);
        assert(prevEuroUlps >= _totalEurUlps);
        uint256 euroUlps = prevEuroUlps - _totalEurUlps;
        emit LogNeumarksBurned(msg.sender, euroUlps, burnNeumarkUlps);
    }
}
contract IFeeDisbursal is IERC223Callback {
}
contract IPlatformPortfolio is IERC223Callback {
}
contract ITokenExchangeRateOracle {
    function getExchangeRate(address numeratorToken, address denominatorToken)
        public
        constant
        returns (uint256 rateFraction, uint256 timestamp);
    function getExchangeRates(address[] numeratorTokens, address[] denominatorTokens)
        public
        constant
        returns (uint256[] rateFractions, uint256[] timestamps);
}
contract Universe is
    Agreement,
    IContractId,
    KnownInterfaces
{
    event LogSetSingleton(
        bytes4 interfaceId,
        address instance,
        address replacedInstance
    );
    event LogSetCollectionInterface(
        bytes4 interfaceId,
        address instance,
        bool isSet
    );
    mapping(bytes4 => address) private _singletons;
    mapping(bytes4 =>
        mapping(address => bool)) private _collections; 
    mapping(address => bytes4[]) private _instances;
    constructor(
        IAccessPolicy accessPolicy,
        IEthereumForkArbiter forkArbiter
    )
        Agreement(accessPolicy, forkArbiter)
        public
    {
        setSingletonPrivate(KNOWN_INTERFACE_ACCESS_POLICY, accessPolicy);
        setSingletonPrivate(KNOWN_INTERFACE_FORK_ARBITER, forkArbiter);
    }
    function getSingleton(bytes4 interfaceId)
        public
        constant
        returns (address)
    {
        return _singletons[interfaceId];
    }
    function getManySingletons(bytes4[] interfaceIds)
        public
        constant
        returns (address[])
    {
        address[] memory addresses = new address[](interfaceIds.length);
        uint256 idx;
        while(idx < interfaceIds.length) {
            addresses[idx] = _singletons[interfaceIds[idx]];
            idx += 1;
        }
        return addresses;
    }
    function isSingleton(bytes4 interfaceId, address instance)
        public
        constant
        returns (bool)
    {
        return _singletons[interfaceId] == instance;
    }
    function isInterfaceCollectionInstance(bytes4 interfaceId, address instance)
        public
        constant
        returns (bool)
    {
        return _collections[interfaceId][instance];
    }
    function isAnyOfInterfaceCollectionInstance(bytes4[] interfaceIds, address instance)
        public
        constant
        returns (bool)
    {
        uint256 idx;
        while(idx < interfaceIds.length) {
            if (_collections[interfaceIds[idx]][instance]) {
                return true;
            }
            idx += 1;
        }
        return false;
    }
    function getInterfacesOfInstance(address instance)
        public
        constant
        returns (bytes4[] interfaces)
    {
        return _instances[instance];
    }
    function setSingleton(bytes4 interfaceId, address instance)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        setSingletonPrivate(interfaceId, instance);
    }
    function setManySingletons(bytes4[] interfaceIds, address[] instances)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        require(interfaceIds.length == instances.length);
        uint256 idx;
        while(idx < interfaceIds.length) {
            setSingletonPrivate(interfaceIds[idx], instances[idx]);
            idx += 1;
        }
    }
    function setCollectionInterface(bytes4 interfaceId, address instance, bool set)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        setCollectionPrivate(interfaceId, instance, set);
    }
    function setInterfaceInManyCollections(bytes4[] interfaceIds, address instance, bool set)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        uint256 idx;
        while(idx < interfaceIds.length) {
            setCollectionPrivate(interfaceIds[idx], instance, set);
            idx += 1;
        }
    }
    function setCollectionsInterfaces(bytes4[] interfaceIds, address[] instances, bool[] set_flags)
        public
        only(ROLE_UNIVERSE_MANAGER)
    {
        require(interfaceIds.length == instances.length);
        require(interfaceIds.length == set_flags.length);
        uint256 idx;
        while(idx < interfaceIds.length) {
            setCollectionPrivate(interfaceIds[idx], instances[idx], set_flags[idx]);
            idx += 1;
        }
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x8b57bfe21a3ef4854e19d702063b6cea03fa514162f8ff43fde551f06372fefd, 0);
    }
    function accessPolicy() public constant returns (IAccessPolicy) {
        return IAccessPolicy(_singletons[KNOWN_INTERFACE_ACCESS_POLICY]);
    }
    function forkArbiter() public constant returns (IEthereumForkArbiter) {
        return IEthereumForkArbiter(_singletons[KNOWN_INTERFACE_FORK_ARBITER]);
    }
    function neumark() public constant returns (Neumark) {
        return Neumark(_singletons[KNOWN_INTERFACE_NEUMARK]);
    }
    function etherToken() public constant returns (IERC223Token) {
        return IERC223Token(_singletons[KNOWN_INTERFACE_ETHER_TOKEN]);
    }
    function euroToken() public constant returns (IERC223Token) {
        return IERC223Token(_singletons[KNOWN_INTERFACE_EURO_TOKEN]);
    }
    function etherLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_ETHER_LOCK];
    }
    function euroLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_EURO_LOCK];
    }
    function icbmEtherLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_ICBM_ETHER_LOCK];
    }
    function icbmEuroLock() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_ICBM_EURO_LOCK];
    }
    function identityRegistry() public constant returns (address) {
        return IIdentityRegistry(_singletons[KNOWN_INTERFACE_IDENTITY_REGISTRY]);
    }
    function tokenExchangeRateOracle() public constant returns (address) {
        return ITokenExchangeRateOracle(_singletons[KNOWN_INTERFACE_TOKEN_EXCHANGE_RATE_ORACLE]);
    }
    function feeDisbursal() public constant returns (address) {
        return IFeeDisbursal(_singletons[KNOWN_INTERFACE_FEE_DISBURSAL]);
    }
    function platformPortfolio() public constant returns (address) {
        return IPlatformPortfolio(_singletons[KNOWN_INTERFACE_PLATFORM_PORTFOLIO]);
    }
    function tokenExchange() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_TOKEN_EXCHANGE];
    }
    function gasExchange() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_GAS_EXCHANGE];
    }
    function platformTerms() public constant returns (address) {
        return _singletons[KNOWN_INTERFACE_PLATFORM_TERMS];
    }
    function setSingletonPrivate(bytes4 interfaceId, address instance)
        private
    {
        require(interfaceId != KNOWN_INTERFACE_UNIVERSE, "NF_UNI_NO_UNIVERSE_SINGLETON");
        address replacedInstance = _singletons[interfaceId];
        if (replacedInstance != instance) {
            dropInstance(replacedInstance, interfaceId);
            addInstance(instance, interfaceId);
            _singletons[interfaceId] = instance;
        }
        emit LogSetSingleton(interfaceId, instance, replacedInstance);
    }
    function setCollectionPrivate(bytes4 interfaceId, address instance, bool set)
        private
    {
        if (_collections[interfaceId][instance] == set) {
            return;
        }
        _collections[interfaceId][instance] = set;
        if (set) {
            addInstance(instance, interfaceId);
        } else {
            dropInstance(instance, interfaceId);
        }
        emit LogSetCollectionInterface(interfaceId, instance, set);
    }
    function addInstance(address instance, bytes4 interfaceId)
        private
    {
        if (instance == address(0)) {
            return;
        }
        bytes4[] storage current = _instances[instance];
        uint256 idx;
        while(idx < current.length) {
            if (current[idx] == interfaceId)
                return;
            idx += 1;
        }
        current.push(interfaceId);
    }
    function dropInstance(address instance, bytes4 interfaceId)
        private
    {
        if (instance == address(0)) {
            return;
        }
        bytes4[] storage current = _instances[instance];
        uint256 idx;
        uint256 last = current.length - 1;
        while(idx <= last) {
            if (current[idx] == interfaceId) {
                if (idx < last) {
                    current[idx] = current[last];
                }
                current.length -= 1;
                return;
            }
            idx += 1;
        }
    }
}
contract ETODurationTerms is IContractId {
    uint32 public WHITELIST_DURATION;
    uint32 public PUBLIC_DURATION;
    uint32 public SIGNING_DURATION;
    uint32 public CLAIM_DURATION;
    constructor(
        uint32 whitelistDuration,
        uint32 publicDuration,
        uint32 signingDuration,
        uint32 claimDuration
    )
        public
    {
        WHITELIST_DURATION = whitelistDuration;
        PUBLIC_DURATION = publicDuration;
        SIGNING_DURATION = signingDuration;
        CLAIM_DURATION = claimDuration;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x5fb50201b453799d95f8a80291b940f1c543537b95bff2e3c78c2e36070494c0, 0);
    }
}
contract ETOTokenTerms is IContractId {
    uint256 public MIN_NUMBER_OF_TOKENS;
    uint256 public MAX_NUMBER_OF_TOKENS;
    uint256 public TOKEN_PRICE_EUR_ULPS;
    uint256 public MAX_NUMBER_OF_TOKENS_IN_WHITELIST;
    uint256 public constant EQUITY_TOKENS_PER_SHARE = 10000;
    uint8 public constant EQUITY_TOKENS_PRECISION = 0; 
    constructor(
        uint256 minNumberOfTokens,
        uint256 maxNumberOfTokens,
        uint256 tokenPriceEurUlps,
        uint256 maxNumberOfTokensInWhitelist
    )
        public
    {
        require(maxNumberOfTokensInWhitelist <= maxNumberOfTokens);
        require(maxNumberOfTokens >= minNumberOfTokens);
        require(minNumberOfTokens >= EQUITY_TOKENS_PER_SHARE, "NF_ETO_TERMS_ONE_SHARE");
        MIN_NUMBER_OF_TOKENS = minNumberOfTokens;
        MAX_NUMBER_OF_TOKENS = maxNumberOfTokens;
        TOKEN_PRICE_EUR_ULPS = tokenPriceEurUlps;
        MAX_NUMBER_OF_TOKENS_IN_WHITELIST = maxNumberOfTokensInWhitelist;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x591e791aab2b14c80194b729a2abcba3e8cce1918be4061be170e7223357ae5c, 0);
    }
}
contract ETOTerms is
    IdentityRecord,
    Math,
    IContractId
{
    struct WhitelistTicket {
        uint128 discountAmountEurUlps;
        uint128 fullTokenPriceFrac;
    }
    bytes32 private constant EMPTY_STRING_HASH = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
    uint256 public constant MIN_QUALIFIED_INVESTOR_TICKET_EUR_ULPS = 100000 * 10**18;
    ETODurationTerms public DURATION_TERMS;
    ETOTokenTerms public TOKEN_TERMS;
    uint256 public EXISTING_COMPANY_SHARES;
    uint256 public SHARE_NOMINAL_VALUE_EUR_ULPS;
    uint256 public MIN_TICKET_EUR_ULPS;
    uint256 public MAX_TICKET_EUR_ULPS;
    uint256 public MAX_TICKET_SIMPLE_EUR_ULPS;
    bool public ENABLE_TRANSFERS_ON_SUCCESS;
    bool public ALLOW_RETAIL_INVESTORS;
    uint256 public WHITELIST_DISCOUNT_FRAC;
    uint256 public PUBLIC_DISCOUNT_FRAC;
    string public INVESTOR_OFFERING_DOCUMENT_URL;
    ShareholderRights public SHAREHOLDER_RIGHTS;
    string public EQUITY_TOKEN_NAME;
    string public EQUITY_TOKEN_SYMBOL;
    address public WHITELIST_MANAGER;
    IIdentityRegistry public IDENTITY_REGISTRY;
    Universe public UNIVERSE;
    uint256 private MIN_NUMBER_OF_TOKENS;
    uint256 private MAX_NUMBER_OF_TOKENS;
    uint256 private TOKEN_PRICE_EUR_ULPS;
    mapping (address => WhitelistTicket) private _whitelist;
    modifier onlyWhitelistManager() {
        require(msg.sender == WHITELIST_MANAGER);
        _;
    }
    event LogInvestorWhitelisted(
        address indexed investor,
        uint256 discountAmountEurUlps,
        uint256 fullTokenPriceFrac
    );
    constructor(
        Universe universe,
        ETODurationTerms durationTerms,
        ETOTokenTerms tokenTerms,
        uint256 existingCompanyShares,
        uint256 minTicketEurUlps,
        uint256 maxTicketEurUlps,
        bool allowRetailInvestors,
        bool enableTransfersOnSuccess,
        string investorOfferingDocumentUrl,
        ShareholderRights shareholderRights,
        string equityTokenName,
        string equityTokenSymbol,
        uint256 shareNominalValueEurUlps,
        uint256 whitelistDiscountFrac,
        uint256 publicDiscountFrac
    )
        public
    {
        require(durationTerms != address(0));
        require(tokenTerms != address(0));
        require(existingCompanyShares > 0);
        require(keccak256(abi.encodePacked(investorOfferingDocumentUrl)) != EMPTY_STRING_HASH);
        require(keccak256(abi.encodePacked(equityTokenName)) != EMPTY_STRING_HASH);
        require(keccak256(abi.encodePacked(equityTokenSymbol)) != EMPTY_STRING_HASH);
        require(shareholderRights != address(0));
        require(shareNominalValueEurUlps > 0);
        require(whitelistDiscountFrac >= 0 && whitelistDiscountFrac <= 99*10**16);
        require(publicDiscountFrac >= 0 && publicDiscountFrac <= 99*10**16);
        require(minTicketEurUlps<=maxTicketEurUlps);
        MIN_NUMBER_OF_TOKENS = tokenTerms.MIN_NUMBER_OF_TOKENS();
        MAX_NUMBER_OF_TOKENS = tokenTerms.MAX_NUMBER_OF_TOKENS();
        TOKEN_PRICE_EUR_ULPS = tokenTerms.TOKEN_PRICE_EUR_ULPS();
        DURATION_TERMS = durationTerms;
        TOKEN_TERMS = tokenTerms;
        EXISTING_COMPANY_SHARES = existingCompanyShares;
        MIN_TICKET_EUR_ULPS = minTicketEurUlps;
        MAX_TICKET_EUR_ULPS = maxTicketEurUlps;
        ALLOW_RETAIL_INVESTORS = allowRetailInvestors;
        ENABLE_TRANSFERS_ON_SUCCESS = enableTransfersOnSuccess;
        INVESTOR_OFFERING_DOCUMENT_URL = investorOfferingDocumentUrl;
        SHAREHOLDER_RIGHTS = shareholderRights;
        EQUITY_TOKEN_NAME = equityTokenName;
        EQUITY_TOKEN_SYMBOL = equityTokenSymbol;
        SHARE_NOMINAL_VALUE_EUR_ULPS = shareNominalValueEurUlps;
        WHITELIST_DISCOUNT_FRAC = whitelistDiscountFrac;
        PUBLIC_DISCOUNT_FRAC = publicDiscountFrac;
        WHITELIST_MANAGER = msg.sender;
        IDENTITY_REGISTRY = IIdentityRegistry(universe.identityRegistry());
        UNIVERSE = universe;
    }
    function calculateTokenAmount(uint256 , uint256 committedEurUlps)
        public
        constant
        returns (uint256 tokenAmountInt)
    {
        return committedEurUlps / calculatePriceFraction(10**18 - PUBLIC_DISCOUNT_FRAC);
    }
    function calculateEurUlpsAmount(uint256 , uint256 tokenAmountInt)
        public
        constant
        returns (uint256 committedEurUlps)
    {
        return mul(tokenAmountInt, calculatePriceFraction(10**18 - PUBLIC_DISCOUNT_FRAC));
    }
    function ESTIMATED_MIN_CAP_EUR_ULPS() public constant returns(uint256) {
        return calculateEurUlpsAmount(0, MIN_NUMBER_OF_TOKENS);
    }
    function ESTIMATED_MAX_CAP_EUR_ULPS() public constant returns(uint256) {
        return calculateEurUlpsAmount(0, MAX_NUMBER_OF_TOKENS);
    }
    function calculatePriceFraction(uint256 priceFrac) public constant returns(uint256) {
        if (priceFrac == 1) {
            return TOKEN_PRICE_EUR_ULPS;
        } else {
            return decimalFraction(priceFrac, TOKEN_PRICE_EUR_ULPS);
        }
    }
    function addWhitelisted(
        address[] investors,
        uint256[] discountAmountsEurUlps,
        uint256[] discountsFrac
    )
        external
        onlyWhitelistManager
    {
        require(investors.length == discountAmountsEurUlps.length);
        require(investors.length == discountsFrac.length);
        for (uint256 i = 0; i < investors.length; i += 1) {
            addWhitelistInvestorPrivate(investors[i], discountAmountsEurUlps[i], discountsFrac[i]);
        }
    }
    function whitelistTicket(address investor)
        public
        constant
        returns (bool isWhitelisted, uint256 discountAmountEurUlps, uint256 fullTokenPriceFrac)
    {
        WhitelistTicket storage wlTicket = _whitelist[investor];
        isWhitelisted = wlTicket.fullTokenPriceFrac > 0;
        discountAmountEurUlps = wlTicket.discountAmountEurUlps;
        fullTokenPriceFrac = wlTicket.fullTokenPriceFrac;
    }
    function calculateContribution(
        address investor,
        uint256 totalContributedEurUlps,
        uint256 existingInvestorContributionEurUlps,
        uint256 newInvestorContributionEurUlps,
        bool applyWhitelistDiscounts
    )
        public
        constant
        returns (
            bool isWhitelisted,
            bool isEligible,
            uint256 minTicketEurUlps,
            uint256 maxTicketEurUlps,
            uint256 equityTokenInt,
            uint256 fixedSlotEquityTokenInt
            )
    {
        (
            isWhitelisted,
            minTicketEurUlps,
            maxTicketEurUlps,
            equityTokenInt,
            fixedSlotEquityTokenInt
        ) = calculateContributionPrivate(
            investor,
            totalContributedEurUlps,
            existingInvestorContributionEurUlps,
            newInvestorContributionEurUlps,
            applyWhitelistDiscounts);
        IdentityClaims memory claims = deserializeClaims(IDENTITY_REGISTRY.getClaims(investor));
        isEligible = claims.isVerified && !claims.accountFrozen;
    }
    function equityTokensToShares(uint256 amount)
        public
        constant
        returns (uint256)
    {
        return divRound(amount, TOKEN_TERMS.EQUITY_TOKENS_PER_SHARE());
    }
    function requireValidTerms(PlatformTerms platformTerms)
        public
        constant
        returns (bool)
    {
        if (ALLOW_RETAIL_INVESTORS) {
            require(!ENABLE_TRANSFERS_ON_SUCCESS, "NF_MUST_DISABLE_TRANSFERS");
        } else {
            require(MIN_TICKET_EUR_ULPS >= MIN_QUALIFIED_INVESTOR_TICKET_EUR_ULPS, "NF_MIN_QUALIFIED_INVESTOR_TICKET");
        }
        require(MIN_TICKET_EUR_ULPS >= TOKEN_TERMS.TOKEN_PRICE_EUR_ULPS(), "NF_MIN_TICKET_LT_TOKEN_PRICE");
        require(ESTIMATED_MAX_CAP_EUR_ULPS() >= MIN_TICKET_EUR_ULPS, "NF_MAX_FUNDS_LT_MIN_TICKET");
        require(MIN_TICKET_EUR_ULPS >= platformTerms.MIN_TICKET_EUR_ULPS(), "NF_ETO_TERMS_MIN_TICKET_EUR_ULPS");
        require(DURATION_TERMS.WHITELIST_DURATION() >= platformTerms.MIN_WHITELIST_DURATION(), "NF_ETO_TERMS_WL_D_MIN");
        require(DURATION_TERMS.WHITELIST_DURATION() <= platformTerms.MAX_WHITELIST_DURATION(), "NF_ETO_TERMS_WL_D_MAX");
        require(DURATION_TERMS.PUBLIC_DURATION() >= platformTerms.MIN_PUBLIC_DURATION(), "NF_ETO_TERMS_PUB_D_MIN");
        require(DURATION_TERMS.PUBLIC_DURATION() <= platformTerms.MAX_PUBLIC_DURATION(), "NF_ETO_TERMS_PUB_D_MAX");
        uint256 totalDuration = DURATION_TERMS.WHITELIST_DURATION() + DURATION_TERMS.PUBLIC_DURATION();
        require(totalDuration >= platformTerms.MIN_OFFER_DURATION(), "NF_ETO_TERMS_TOT_O_MIN");
        require(totalDuration <= platformTerms.MAX_OFFER_DURATION(), "NF_ETO_TERMS_TOT_O_MAX");
        require(DURATION_TERMS.SIGNING_DURATION() >= platformTerms.MIN_SIGNING_DURATION(), "NF_ETO_TERMS_SIG_MIN");
        require(DURATION_TERMS.SIGNING_DURATION() <= platformTerms.MAX_SIGNING_DURATION(), "NF_ETO_TERMS_SIG_MAX");
        require(DURATION_TERMS.CLAIM_DURATION() >= platformTerms.MIN_CLAIM_DURATION(), "NF_ETO_TERMS_CLAIM_MIN");
        require(DURATION_TERMS.CLAIM_DURATION() <= platformTerms.MAX_CLAIM_DURATION(), "NF_ETO_TERMS_CLAIM_MAX");
        return true;
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0x3468b14073c33fa00ee7f8a289b14f4a10c78ab72726033b27003c31c47b3f6a, 0);
    }
    function calculateContributionPrivate(
        address investor,
        uint256 totalContributedEurUlps,
        uint256 existingInvestorContributionEurUlps,
        uint256 newInvestorContributionEurUlps,
        bool applyWhitelistDiscounts
    )
        private
        constant
        returns (
            bool isWhitelisted,
            uint256 minTicketEurUlps,
            uint256 maxTicketEurUlps,
            uint256 equityTokenInt,
            uint256 fixedSlotEquityTokenInt
        )
    {
        uint256 discountedAmount;
        minTicketEurUlps = MIN_TICKET_EUR_ULPS;
        maxTicketEurUlps = MAX_TICKET_EUR_ULPS;
        WhitelistTicket storage wlTicket = _whitelist[investor];
        isWhitelisted = wlTicket.fullTokenPriceFrac > 0;
        if (applyWhitelistDiscounts) {
            maxTicketEurUlps = max(wlTicket.discountAmountEurUlps, maxTicketEurUlps);
            if (wlTicket.discountAmountEurUlps > 0) {
                minTicketEurUlps = min(wlTicket.discountAmountEurUlps, minTicketEurUlps);
            }
            if (existingInvestorContributionEurUlps < wlTicket.discountAmountEurUlps) {
                discountedAmount = min(newInvestorContributionEurUlps, wlTicket.discountAmountEurUlps - existingInvestorContributionEurUlps);
                if (discountedAmount > 0) {
                    fixedSlotEquityTokenInt = discountedAmount / calculatePriceFraction(wlTicket.fullTokenPriceFrac);
                }
            }
        }
        uint256 remainingAmount = newInvestorContributionEurUlps - discountedAmount;
        if (remainingAmount > 0) {
            if (applyWhitelistDiscounts && WHITELIST_DISCOUNT_FRAC > 0) {
                equityTokenInt = remainingAmount / calculatePriceFraction(10**18 - WHITELIST_DISCOUNT_FRAC);
            } else {
                equityTokenInt = calculateTokenAmount(totalContributedEurUlps + discountedAmount, remainingAmount);
            }
        }
        equityTokenInt += fixedSlotEquityTokenInt;
    }
    function addWhitelistInvestorPrivate(
        address investor,
        uint256 discountAmountEurUlps,
        uint256 fullTokenPriceFrac
    )
        private
    {
        require(investor != address(0));
        require(fullTokenPriceFrac > 0 && fullTokenPriceFrac <= 10**18, "NF_DISCOUNT_RANGE");
        require(discountAmountEurUlps < 2**128);
        _whitelist[investor] = WhitelistTicket({
            discountAmountEurUlps: uint128(discountAmountEurUlps),
            fullTokenPriceFrac: uint128(fullTokenPriceFrac)
        });
        emit LogInvestorWhitelisted(investor, discountAmountEurUlps, fullTokenPriceFrac);
    }
}
contract ICommitment is
    IAgreement,
    IERC223Callback
{
    event LogFundsCommitted(
        address indexed investor,
        address wallet,
        address paymentToken,
        uint256 amount,
        uint256 baseCurrencyEquivalent,
        uint256 grantedAmount,
        address assetToken,
        uint256 neuReward
    );
    function finalized() public constant returns (bool);
    function success() public constant returns (bool);
    function failed() public constant returns (bool);
    function totalInvestment()
        public
        constant
        returns (
            uint256 totalEquivEurUlps,
            uint256 totalTokensInt,
            uint256 totalInvestors
        );
    function tokenFallback(address investor, uint256 amount, bytes data)
        public;
}
contract IETOCommitment is
    ICommitment,
    IETOCommitmentStates
{
    event LogStateTransition(
        uint32 oldState,
        uint32 newState,
        uint32 timestamp
    );
    event LogTokensClaimed(
        address indexed investor,
        address indexed assetToken,
        uint256 amount,
        uint256 nmkReward
    );
    event LogFundsRefunded(
        address indexed investor,
        address indexed paymentToken,
        uint256 amount
    );
    event LogTermsSet(
        address companyLegalRep,
        address etoTerms,
        address equityToken
    );
    event LogETOStartDateSet(
        address companyLegalRep,
        uint256 previousTimestamp,
        uint256 newTimestamp
    );
    event LogSigningStarted(
        address nominee,
        address companyLegalRep,
        uint256 newShares,
        uint256 capitalIncreaseEurUlps
    );
    event LogCompanySignedAgreement(
        address companyLegalRep,
        address nominee,
        string signedInvestmentAgreementUrl
    );
    event LogNomineeConfirmedAgreement(
        address nominee,
        address companyLegalRep,
        string signedInvestmentAgreementUrl
    );
    event LogRefundStarted(
        address assetToken,
        uint256 totalTokenAmountInt,
        uint256 totalRewardNmkUlps
    );
    function state() public constant returns (ETOState);
    function startOf(ETOState s) public constant returns (uint256);
    function commitmentObserver() public constant returns (IETOCommitmentObserver);
    function refund() external;
    function refundMany(address[] investors) external;
    function claim() external;
    function claimMany(address[] investors) external;
    function payout() external;
    function etoTerms() public constant returns (ETOTerms);
    function equityToken() public constant returns (IEquityToken);
    function nominee() public constant returns (address);
    function companyLegalRep() public constant returns (address);
    function signedInvestmentAgreementUrl() public constant returns (string);
    function contributionSummary()
        public
        constant
        returns (
            uint256 newShares, uint256 capitalIncreaseEurUlps,
            uint256 additionalContributionEth, uint256 additionalContributionEurUlps,
            uint256 tokenParticipationFeeInt, uint256 platformFeeEth, uint256 platformFeeEurUlps,
            uint256 sharePriceEurUlps
        );
    function investorTicket(address investor)
        public
        constant
        returns (
            uint256 equivEurUlps,
            uint256 rewardNmkUlps,
            uint256 equityTokenInt,
            uint256 sharesInt,
            uint256 tokenPrice,
            uint256 neuRate,
            uint256 amountEth,
            uint256 amountEurUlps,
            bool claimOrRefundSettled,
            bool usedLockedAccount
        );
}
contract IControllerGovernance is
    IAgreement
{
    enum GovState {
        Setup, 
        Offering, 
        Funded, 
        Closing, 
        Closed, 
        Migrated 
    }
    enum Action {
        None, 
        StopToken, 
        ContinueToken, 
        CloseToken, 
        Payout, 
        RegisterOffer, 
        ChangeTokenController, 
        AmendISHA, 
        IssueTokensForExistingShares, 
        ChangeNominee,
        Downround 
    }
    event LogGovStateTransition(
        uint32 oldState,
        uint32 newState,
        uint32 timestamp
    );
    event LogResolutionExecuted(
        bytes32 resolutionId,
        Action action
    );
    event LogTransfersStateChanged(
        bytes32 resolutionId,
        address equityToken,
        bool transfersEnabled
    );
    event LogISHAAmended(
        bytes32 resolutionId,
        string ISHAUrl,
        uint256 totalShares,
        uint256 companyValuationEurUlps,
        address newShareholderRights
    );
    event LogOfferingFailed(
        address etoCommitment,
        address equityToken
    );
    event LogOfferingSucceeded(
        address etoCommitment,
        address equityToken,
        uint256 newShares
    );
    event LogGeneralInformation(
        address companyLegalRep,
        string informationType,
        string informationUrl
    );
    event LogOfferingRegistered(
        bytes32 resolutionId,
        address etoCommitment,
        address equityToken
    );
    event LogMigratedTokenController(
        bytes32 resolutionId,
        address newController
    );
    function state()
        public
        constant
        returns (GovState);
    function companyLegalRepresentative()
        public
        constant
        returns (address);
    function shareholderInformation()
        public
        constant
        returns (
            uint256 totalCompanyShares,
            uint256 companyValuationEurUlps,
            ShareholderRights shareholderRights
        );
    function capTable()
        public
        constant
        returns (
            address[] equityTokens,
            uint256[] shares
        );
    function tokenOfferings()
        public
        constant
        returns (
            address[] offerings,
            address[] equityTokens
        );
    function issueGeneralInformation(
        string informationType,
        string informationUrl
    )
        public;
    function startResolution(string title, string resolutionUri, Action action, bytes payload)
        public
        returns (bytes32 resolutionId);
    function executeResolution(bytes32 resolutionId) public;
    function closeCompany() public;
    function cancelCompanyClosing() public;
    function changeTokenController(address newController) public;
    function newTokenController() public constant returns (address);
    function oldTokenController() public constant returns (address);
}
contract PlaceholderEquityTokenController is
    IEquityTokenController,
    IControllerGovernance,
    IContractId,
    Agreement,
    KnownInterfaces
{
    Universe private UNIVERSE;
    address private COMPANY_LEGAL_REPRESENTATIVE;
    GovState private _state;
    uint256 private _totalCompanyShares;
    uint256 private _companyValuationEurUlps;
    ShareholderRights private _shareholderRights;
    address private _newController;
    IEquityToken private _equityToken;
    address private _commitment;
    bool private _transfersEnabled;
    modifier onlyUniverseETO() {
        require(UNIVERSE.isInterfaceCollectionInstance(KNOWN_INTERFACE_COMMITMENT, msg.sender), "NF_ETC_ETO_NOT_U");
        _;
    }
    modifier onlyCompany() {
        require(msg.sender == COMPANY_LEGAL_REPRESENTATIVE, "NF_ONLY_COMPANY");
        _;
    }
    modifier onlyOperational() {
        require(_state == GovState.Offering || _state == GovState.Funded || _state == GovState.Closing, "NF_INV_STATE");
        _;
    }
    modifier onlyState(GovState state) {
        require(_state == state, "NF_INV_STATE");
        _;
    }
    modifier onlyStates(GovState state1, GovState state2) {
        require(_state == state1 || _state == state2, "NF_INV_STATE");
        _;
    }
    constructor(
        Universe universe,
        address companyLegalRep
    )
        public
        Agreement(universe.accessPolicy(), universe.forkArbiter())
    {
        UNIVERSE = universe;
        COMPANY_LEGAL_REPRESENTATIVE = companyLegalRep;
    }
    function state()
        public
        constant
        returns (GovState)
    {
        return _state;
    }
    function companyLegalRepresentative()
        public
        constant
        returns (address)
    {
        return COMPANY_LEGAL_REPRESENTATIVE;
    }
    function shareholderInformation()
        public
        constant
        returns (
            uint256 totalCompanyShares,
            uint256 companyValuationEurUlps,
            ShareholderRights shareholderRights
        )
    {
        return (
            _totalCompanyShares,
            _companyValuationEurUlps,
            _shareholderRights
        );
    }
    function capTable()
        public
        constant
        returns (
            address[] equityTokens,
            uint256[] shares
        )
    {
        if (_state == GovState.Setup || _state == GovState.Offering) {
            return;
        }
        equityTokens = new address[](1);
        shares = new uint256[](1);
        equityTokens[0] = _equityToken;
        shares[0] = _equityToken.sharesTotalSupply();
    }
    function tokenOfferings()
        public
        constant
        returns (
            address[] offerings,
            address[] equityTokens
        )
    {
        if (_state == GovState.Setup) {
            return;
        }
        offerings = new address[](1);
        equityTokens = new address[](1);
        equityTokens[0] = _equityToken;
        offerings[0] = _commitment;
    }
    function issueGeneralInformation(
        string informationType,
        string informationUrl
    )
        public
        onlyOperational
        onlyCompany
    {
        emit LogGeneralInformation(COMPANY_LEGAL_REPRESENTATIVE, informationType, informationUrl);
    }
    function startResolution(string , string , Action , bytes )
        public
        onlyStates(GovState.Offering, GovState.Funded)
        onlyCompany
        returns (bytes32 )
    {
        revert("NF_NOT_IMPL");
    }
    function executeResolution(bytes32 )
        public
        onlyOperational
    {
        revert("NF_NOT_IMPL");
    }
    function closeCompany()
        public
        onlyState(GovState.Closing)
    {
        revert("NF_NOT_IMPL");
    }
    function cancelCompanyClosing()
        public
        onlyState(GovState.Closing)
    {
        revert("NF_NOT_IMPL");
    }
    function changeTokenController(address newController)
        public
        onlyState(GovState.Funded)
        onlyCompany
    {
        require(newController != address(0));
        require(newController != address(this));
        _newController = newController;
        transitionTo(GovState.Migrated);
        emit LogResolutionExecuted(0, Action.ChangeTokenController);
        emit LogMigratedTokenController(0, newController);
    }
    function newTokenController()
        public
        constant
        returns (address)
    {
        return _newController;
    }
    function oldTokenController()
        public
        constant
        returns (address)
    {
        return address(0);
    }
    function onTransfer(address broker, address from, address , uint256 )
        public
        constant
        returns (bool allow)
    {
        return _transfersEnabled || (from == _commitment && broker == from);
    }
    function onApprove(address, address, uint256)
        public
        constant
        returns (bool allow)
    {
        return true;
    }
    function onGenerateTokens(address sender, address, uint256)
        public
        constant
        returns (bool allow)
    {
        return sender == _commitment && _state == GovState.Offering;
    }
    function onDestroyTokens(address sender, address, uint256)
        public
        constant
        returns (bool allow)
    {
        return sender == _commitment && _state == GovState.Offering;
    }
    function onChangeTokenController(address , address newController)
        public
        constant
        returns (bool)
    {
        return newController == _newController;
    }
    function onAllowance(address , address )
        public
        constant
        returns (uint256)
    {
        return 0;
    }
    function onChangeNominee(address, address, address)
        public
        constant
        returns (bool)
    {
        return false;
    }
    function tokenFallback(address, uint256, bytes)
        public
    {
        revert("NF_NOT_IMPL");
    }
    function commitmentObserver() public
        constant
        returns (address)
    {
        return _commitment;
    }
    function onStateTransition(ETOState, ETOState newState)
        public
        onlyUniverseETO
    {
        if (newState == ETOState.Whitelist) {
            require(_state == GovState.Setup, "NF_ETC_BAD_STATE");
            registerTokenOfferingPrivate(IETOCommitment(msg.sender));
            return;
        }
        require(msg.sender == _commitment, "NF_ETC_UNREG_COMMITMENT");
        if (newState == ETOState.Claim) {
            require(_state == GovState.Offering, "NF_ETC_BAD_STATE");
            aproveTokenOfferingPrivate(IETOCommitment(msg.sender));
        }
        if (newState == ETOState.Refund) {
            require(_state == GovState.Offering, "NF_ETC_BAD_STATE");
            failTokenOfferingPrivate(IETOCommitment(msg.sender));
        }
    }
    function contractId() public pure returns (bytes32 id, uint256 version) {
        return (0xf7e00d1a4168be33cbf27d32a37a5bc694b3a839684a8c2bef236e3594345d70, 0);
    }
    function newOffering(IEquityToken equityToken, address tokenOffering)
        internal
    {
        _equityToken = equityToken;
        _commitment = tokenOffering;
        emit LogResolutionExecuted(0, Action.RegisterOffer);
        emit LogOfferingRegistered(0, tokenOffering, equityToken);
    }
    function amendISHA(
        string memory ISHAUrl,
        uint256 totalShares,
        uint256 companyValuationEurUlps,
        ShareholderRights newShareholderRights
    )
        internal
    {
        this.amendAgreement(ISHAUrl);
        _totalCompanyShares = totalShares;
        _companyValuationEurUlps = companyValuationEurUlps;
        _shareholderRights = newShareholderRights;
        emit LogResolutionExecuted(0, Action.AmendISHA);
        emit LogISHAAmended(0, ISHAUrl, totalShares, companyValuationEurUlps, newShareholderRights);
    }
    function enableTransfers(bool transfersEnabled)
        internal
    {
        if (_transfersEnabled != transfersEnabled) {
            _transfersEnabled = transfersEnabled;
        }
        emit LogResolutionExecuted(0, transfersEnabled ? Action.ContinueToken : Action.StopToken);
        emit LogTransfersStateChanged(0, _equityToken, transfersEnabled);
    }
    function transitionTo(GovState newState)
        internal
    {
        emit LogGovStateTransition(uint32(_state), uint32(newState), uint32(block.timestamp));
        _state = newState;
    }
    function mCanAmend(address legalRepresentative)
        internal
        returns (bool)
    {
        return legalRepresentative == address(this);
    }
    function registerTokenOfferingPrivate(IETOCommitment tokenOffering)
        private
    {
        IEquityToken equityToken = tokenOffering.equityToken();
        (address nomineeToken,,,) = equityToken.currentAgreement();
        require(equityToken.tokenController() == address(this), "NF_NDT_ET_TC_MIS");
        (address nomineOffering,,,) = tokenOffering.currentAgreement();
        require(nomineOffering == nomineeToken, "NF_NDT_ETO_A_MIS");
        require(tokenOffering.etoTerms() != address(0), "NF_NDT_ETO_NO_TERMS");
        require(tokenOffering.companyLegalRep() == COMPANY_LEGAL_REPRESENTATIVE, "NF_NDT_ETO_LREP_MIS");
        newOffering(equityToken, tokenOffering);
        transitionTo(GovState.Offering);
    }
    function aproveTokenOfferingPrivate(IETOCommitment tokenOffering)
        private
    {
        (uint256 newShares,,,,,,,) = tokenOffering.contributionSummary();
        uint256 totalShares = tokenOffering.etoTerms().EXISTING_COMPANY_SHARES() + newShares;
        uint256 marginalTokenPrice = tokenOffering.etoTerms().TOKEN_TERMS().TOKEN_PRICE_EUR_ULPS();
        string memory ISHAUrl = tokenOffering.signedInvestmentAgreementUrl();
        amendISHA(
            ISHAUrl,
            totalShares,
            totalShares * marginalTokenPrice * tokenOffering.etoTerms().TOKEN_TERMS().EQUITY_TOKENS_PER_SHARE(),
            tokenOffering.etoTerms().SHAREHOLDER_RIGHTS()
        );
        enableTransfers(tokenOffering.etoTerms().ENABLE_TRANSFERS_ON_SUCCESS());
        transitionTo(GovState.Funded);
        emit LogOfferingSucceeded(tokenOffering, tokenOffering.equityToken(), newShares);
    }
    function failTokenOfferingPrivate(IETOCommitment tokenOffering)
        private
    {
        _equityToken = IEquityToken(0);
        _commitment = IETOCommitment(0);
        _totalCompanyShares = 0;
        _companyValuationEurUlps = 0;
        transitionTo(GovState.Setup);
        emit LogOfferingFailed(tokenOffering, tokenOffering.equityToken());
    }
}
```

## RQ1_1d05ec2e6d83

SHA-256 `bc2456c64a61563a3c0f4b49862caebe06aec843e38e5394111f6eb5573194ac`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
 function div(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b > 0); 
    uint256 c = a / b;
    assert(a == b * c + a % b); 
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
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
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
interface OLdxrpct {
    function transfer(address receiver, uint amount) external;
    function balanceOf(address _owner) external returns (uint256 balance);
    function mint(address wallet, address buyer, uint256 tokenAmount) external;
    function showMyTokenBalance(address addr) external;
}
contract Nyomi is ERC20Interface,Ownable {
   using SafeMath for uint256;
    uint256 public totalSupply;
    mapping(address => uint256) tokenBalances;
   string public constant name = "NyomiToken";
   string public constant symbol = "Nyo";
   uint256 public constant decimals = 18;
   uint256 public constant INITIAL_SUPPLY = 1000000000;
    address ownerWallet;
   mapping (address => mapping (address => uint256)) allowed;
   event Debug(string message, address addr, uint256 number);
    function MADToken(address wallet) public {
        owner = msg.sender;
        ownerWallet=wallet;
        totalSupply = INITIAL_SUPPLY * 10 ** 18;
        tokenBalances[wallet] = INITIAL_SUPPLY * 10 ** 18;   
    }
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(tokenBalances[msg.sender]>=_value);
    tokenBalances[msg.sender] = tokenBalances[msg.sender].sub(_value);
    tokenBalances[_to] = tokenBalances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= tokenBalances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    tokenBalances[_from] = tokenBalances[_from].sub(_value);
    tokenBalances[_to] = tokenBalances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
     function totalSupply() public constant returns (uint) {
         return totalSupply  - tokenBalances[address(0)];
     }
     function allowance(address tokenOwner, address spender) public constant returns (uint remaining) {
         return allowed[tokenOwner][spender];
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
     function () public payable {
         revert();
     }
  function balanceOf(address _owner) constant public returns (uint256 balance) {
    return tokenBalances[_owner];
  }
    function mint(address wallet, address buyer, uint256 tokenAmount) public onlyOwner {
      require(tokenBalances[wallet] >= tokenAmount);               
      tokenBalances[buyer] = tokenBalances[buyer].add(tokenAmount);                  
      tokenBalances[wallet] = tokenBalances[wallet].sub(tokenAmount);                        
      Transfer(wallet, buyer, tokenAmount); 
      totalSupply=totalSupply.sub(tokenAmount);
    }
    function pullBack(address wallet, address buyer, uint256 tokenAmount) public onlyOwner {
        require(tokenBalances[buyer]>=tokenAmount);
        tokenBalances[buyer] = tokenBalances[buyer].sub(tokenAmount);
        tokenBalances[wallet] = tokenBalances[wallet].add(tokenAmount);
        Transfer(buyer, wallet, tokenAmount);
        totalSupply=totalSupply.add(tokenAmount);
     }
    function showMyTokenBalance(address addr) public view returns (uint tokenBalance) {
        tokenBalance = tokenBalances[addr];
    }
}
```

## RQ1_0a67a2a6aa84

SHA-256 `01f3ce702b1d3adfc9bc00eec7fba9ded3f3c4e54685453973127808a8fab102`

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
contract Globextoken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "GLOBEX";
    string public constant symbol = "GEX";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
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
    function GEXGLOBEXTOKEN () public {
        owner = msg.sender;
        uint256 TeamTokens = 9000000000e8;
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

## RQ1_4280173fabd7

SHA-256 `13aac2c757c049ec966ab41619ed44adae401ef402aeaca473cd92b397f0f2d7`

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
    event EventLuckyNumberUpdated(uint256 cost, uint256 max, uint8 waitTime);
    event EventLuckyNumberRequested(address requestor, uint256 max, uint256 creationBlockNumber, uint8 waitTime);
    event EventLuckyNumberRevealed(address requestor, uint256 max, uint256 renderedNumber);
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
        pendingNumbers[_requestor].creationBlockNumber = 0;
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

## RQ1_447aa12a3c06

SHA-256 `5b9db5f8f8e5c0531b346db8d9715895392364d380155e6ad5ac76cd4a4611cc`

```solidity
pragma solidity 0.4.23;
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
	using SafeMath for uint256;
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
        require(balanceOf[_to].add(_value) > balanceOf[_to]);
        uint previousBalances = balanceOf[_from].add(balanceOf[_to]);
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        Transfer(_from, _to, _value);
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
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                
        require(_value <= allowance[_from][msg.sender]);    
        balanceOf[_from] = balanceOf[_from].sub(_value);                         
        allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);             
        totalSupply = totalSupply.sub(_value);                              
        Burn(_from, _value);
        return true;
    }
}
contract CRYPTOBITECOIN is owned, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
	using SafeMath for uint256;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool frozen);
    function CRYPTOBITECOIN(
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
        balanceOf[_to] = balanceOf[_from].add(_value);                           
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
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    function buy() payable public {
        uint amount = msg.value.div(buyPrice);               
        _transfer(this, msg.sender, amount);              
    }
    function sell(uint256 amount) public {
        require(this.balance >= amount.mul(sellPrice));      
        _transfer(msg.sender, this, amount);              
        msg.sender.transfer(amount * sellPrice);          
    }
}
```

## RQ1_14285ee7645a

SHA-256 `12e3b34f8da66b16f90bdef7dcede565bf8d362ae45bba41eb9f9eb2c780f729`

```solidity
pragma solidity ^0.4.13;
contract DaoToken {
  uint256 public CAP;
  uint256 public totalEthers;
  function proxyPayment(address participant) payable;
  function transfer(address _to, uint _amount) returns (bool success);
}
contract ZiberToken {
  mapping (address => uint256) public balances;
  mapping (address => bool) public checked_in;
  uint256 public ico;
  bool public bought_tokens;
  uint256 public time_bought;
  uint256 public extra_time_bought;
  bool public kill_switch;
  string public name;
  string public symbol;
  uint8 public decimals;
  uint256 ZBR_per_eth = 17440;
  uint256 ZBR_total_reserve = 100000000;
  uint256 ZBR_dev_reserved = 10000000;
  uint256 ZBR_for_selling = 80000000;
  uint256 ZBR_for_ico= 10000000;
  uint256 min_eth_to_end = 50000 ether;
  uint256 max_eth_to_end = 100000 ether;
  uint registredTo;
  uint256 loadedRefund;
  uint256 _supply;
  string _name;
  string _symbol;
  uint8 _decimals;
  DaoToken public token = DaoToken(0xa9d585CE3B227d69985c3F7A866fE7d0e510da50);
  address developer_address = 0x004B74Ea737AFD25ce083573fB45a49da762aCD4; 
  mapping (address => uint256) public balanceOf;
  event Transfer(address indexed from, address indexed to, uint256 value);
  function ZiberToken() {
      _supply = 10000000000;
      balanceOf[msg.sender] = _supply;
      name = "ZIBER LTD Crowdsale Tokens";     
      symbol = "ZBR";
      decimals = 2;
  }
  function safeMul(uint a, uint b) internal returns (uint) {
    uint c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function safeDiv(uint a, uint b) internal returns (uint) {
    assert(b > 0);
    uint c = a / b;
    assert(a == b * c + a % b);
    return c;
  }
  function safeSub(uint a, uint b) internal returns (uint) {
    assert(b <= a);
    return a - b;
  }
  function safeAdd(uint a, uint b) internal returns (uint) {
    uint c = a + b;
    assert(c>=a && c>=b);
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
  function loadRefund() payable {
    if(msg.value == 0) throw;
    loadedRefund = safeAdd(loadedRefund, msg.value);
  }
  function refund() private  {
    uint256 weiValue = this.balance;
    if (weiValue == 0) throw;
    uint256 weiRefunded;
    weiRefunded = safeAdd(weiRefunded, weiValue);
    refund();
    if (!msg.sender.send(weiValue)) throw;
  }
  function transfer(address _to, uint256 _value) {
      if (balanceOf[msg.sender] < _value) throw;
      if (balanceOf[_to] + _value < balanceOf[_to]) throw;
      balanceOf[msg.sender] -= _value;
      balanceOf[_to] += _value;
      Transfer(msg.sender, _to, _value);
  }
  function activate_kill_switch() {
    if (msg.sender != developer_address) throw;
    kill_switch = true;
  }
  function withdraw(){
    if (!bought_tokens) {
      uint256 eth_amount = balances[msg.sender];
      balances[msg.sender] = 0;
      msg.sender.transfer(eth_amount);
    }
    else {
      uint256 ZBR_amount = balances[msg.sender] * ZBR_per_eth;
      balances[msg.sender] = 0;
      uint256 fee = 0;
      if (!checked_in[msg.sender]) {
        fee = ZBR_amount / 100;
        if(!token.transfer(developer_address, fee)) throw;
      }
      if(!token.transfer(msg.sender, ZBR_amount - fee)) throw;
    }
  }
  function add_to_ico() payable {
    if (msg.sender != developer_address) throw;
    if (kill_switch) throw;
    if (bought_tokens) throw;
    ico += msg.value;
  }
  function claim_ico(){
    if (bought_tokens) return;
    if (kill_switch) throw;
    bought_tokens = true;
    time_bought = now + 1 days;
    token.proxyPayment.value(this.balance - ico)(address(this));
    if(this.balance > max_eth_to_end)
    {
        msg.sender.transfer(ico);
    }
    else {
        extra_time_bought = now +  1 days * 10;
        if(this.balance < min_eth_to_end) throw;
        else {
          if (now > extra_time_bought) {
            msg.sender.transfer(ico);
          }
        }
      }
  }
  modifier onlyOwner() {
    if (msg.sender != developer_address) {
      throw;
    }
    _;
  }
  function withdrawEth() onlyOwner {        
        msg.sender.transfer(this.balance);
  }
  function kill() onlyOwner {        
        selfdestruct(developer_address);
  }
  function default_helper() payable {
    if (now < 1500655200 ) throw; 
    else {
      if (msg.value <= 1 finney) {
        if (bought_tokens) {
          if (token.totalEthers() >= token.CAP()) throw;
          checked_in[msg.sender] = true;
        }
        else {
          withdraw();
        }
      }
      else {
        if (kill_switch) throw;
        if (bought_tokens) throw;
        balances[msg.sender] += msg.value;
      }
    }
  }
  function () payable {
    default_helper();
  }
}
```

## RQ1_0e842b26f8af

SHA-256 `613a35a75143a063dbeee30925fa6dd190ed0ffc643762d23a49904489babc8c`

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
contract TOXTToken is StandardToken {
  string public name = 'TOXbtc Token';
  string public symbol = 'TOXT';
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
  function TOXTToken() public {
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

## RQ1_affea7f70c2f

SHA-256 `6876c6bc2d44e330e8fb877b914cf6392a1d580a5e734620aa6ce86a706928ea`

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
contract RethenToken is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "Rethen Token";
    string public constant symbol = "RETHEN1";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 200000000e8;
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
    function Rethen () public {
        owner = msg.sender;
        uint256 devTokens = 2500000000e8;
        distr(owner, devTokens);
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
        Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_e174c093cc1b

SHA-256 `613e876e833fffb748d99df2131cd44b935b52369fe616630bb83039dd80b62d`

```solidity
pragma solidity ^0.4.19;
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
    function distr(address _to, uint256 _value) public returns (bool);
    function totalSupply() constant public returns (uint256 supply);
    function balanceOf(address _owner) constant public returns (uint256 balance);
}
contract BECHAIN is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "BECHAIN";
    string public constant symbol = "BCN";
    uint public constant decimals = 8;
        uint256 public totalSupply = 2000000000e8;
    uint256 public totalDistributed = 200000000e8;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
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
    function BEN () public {
        owner = msg.sender;
        value = 4000e8;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function enableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = false;
        }
    }
    function disableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = true;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function airdrop(address[] addresses) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(value <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(value <= totalRemaining);
            distr(addresses[i], value);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distribution(address[] addresses, uint256 amount) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(amount <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(amount <= totalRemaining);
            distr(addresses[i], amount);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            require(amounts[i] <= totalRemaining);
            distr(addresses[i], amounts[i]);
            if (totalDistributed >= totalSupply) {
                distributionFinished = true;
            }
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
        uint256 etherBalance = this.balance;
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

## RQ1_cd4f6d82bc67

SHA-256 `3a6ca798dfc265b9875f1c2cdcc6a2acabecbe7572b55489639e0afeb2330204`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
  function mul(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a / b;
    return c;
  }
  function sub(uint256 a, uint256 b) internal constant returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal constant returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function Ownable() {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
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
contract BasicToken is ERC20Basic, Ownable {
  using SafeMath for uint256;
  mapping(address => uint256) balances;
  mapping(address => bool) locks;
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(!locks[msg.sender] && !locks[_to]);
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }
  function balanceOf(address _owner) public constant returns (uint256 balance) {
    return balances[_owner];
  }
  function setLock(address _toLock, bool _setTo) onlyOwner {
      locks[_toLock] = _setTo;
  }
  function lockOf(address _owner) public constant returns (bool lock) {
    return locks[_owner];
  }
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) internal allowed;
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(!locks[_from] && !locks[_to]);
    uint256 _allowance = allowed[_from][msg.sender];
    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = _allowance.sub(_value);
    Transfer(_from, _to, _value);
    return true;
  }
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
    return allowed[_owner][_spender];
  }
  function increaseApproval (address _spender, uint _addedValue) public returns (bool success) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
  function decreaseApproval (address _spender, uint _subtractedValue) public returns (bool success) {
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
contract MintableToken is StandardToken {
  string public constant name = "CryptoTask";
  string public constant symbol = "CTF";
  uint8 public constant decimals = 18; 
  event Mint(address indexed to, uint256 amount);
  event MintFinished();
  bool public mintingFinished = false;
  modifier canMint() {
    require(!mintingFinished);
    _;
  }
  function mint(address _to, uint256 _amount) onlyOwner canMint public returns (bool) {
    require(!locks[_to]);
    totalSupply = totalSupply.add(_amount);
    balances[_to] = balances[_to].add(_amount);
    Mint(_to, _amount);
    Transfer(0x0, _to, _amount);
    return true;
  }
  function finishMinting() onlyOwner public returns (bool) {
    mintingFinished = true;
    MintFinished();
    return true;
  }
}
contract Crowdsale is Ownable {
    using SafeMath for uint;
    uint public fundingGoal = 1000 * 1 ether;
    uint public hardCap;
    uint public amountRaisedPreSale = 0;
    uint public amountRaisedICO = 0;
    uint public contractDeployedTime;
    uint presaleDuration = 30 * 1 days;
    uint countdownDuration = 45 * 1 days;
    uint icoDuration = 20 * 1 days;
    uint public presaleEndTime;
    uint public deadline;
    uint public price = (1 ether)/1000;
    MintableToken public token;
    mapping(address => uint) public balanceOf;
    bool public icoSuccess = false;
    bool public crowdsaleClosed = false;
    address vault1;
    address vault2 = 0xC0776D495f9Ed916C87c8C48f34f08E2B9506342;
    uint public stage = 0;
    uint public against = 0;
    uint public lastVoteTime;
    uint minVoteTime = 180 * 1 days;
    event GoalReached(uint amountRaised);
    event FundTransfer(address backer, uint amount, bool isContribution);
    function Crowdsale() {
        contractDeployedTime = now;
        vault1 = msg.sender;
        token = new MintableToken();
    }
    function () payable {
        require(!token.lockOf(msg.sender) && !crowdsaleClosed && stage<2 && msg.value >= 1 * (1 ether)/10);
        if(stage==1 && (now < presaleEndTime.add(countdownDuration) || amountRaisedPreSale+amountRaisedICO+msg.value > hardCap)) {
            throw;
        }
        uint amount = msg.value;
        balanceOf[msg.sender] += amount;
        if(stage==0) {  
            amountRaisedPreSale += amount;
            token.mint(msg.sender, amount.mul(2) / price);
        } else {
            amountRaisedICO += amount;
            token.mint(msg.sender, amount / price);
        }
        FundTransfer(msg.sender, amount, true);
    }
    function forward(uint amount) internal {
        vault1.transfer(amount.mul(67)/100);
        vault2.transfer(amount.sub(amount.mul(67)/100));
    }
    modifier afterDeadline() { if (stage > 0 && now >= deadline) {_;} }
    function checkGoalReached() afterDeadline {
        require(stage==1 && !crowdsaleClosed);
        if (amountRaisedPreSale+amountRaisedICO >= fundingGoal) {
            uint amount = amountRaisedICO/3;
            if(!icoSuccess) {
                amount += amountRaisedPreSale/3;    
            }
            uint amountToken1 = token.totalSupply().mul(67)/(100*4);
            uint amountToken2 = token.totalSupply().mul(33)/(100*4);
            forward(amount);
            icoSuccess = true;
            token.mint(vault1, amountToken1);    
            token.mint(vault2, amountToken2);    
            stage=2;
            lastVoteTime = now;
            GoalReached(amountRaisedPreSale+amountRaisedICO);
        }
        crowdsaleClosed = true;
        token.finishMinting();
    }
    function closePresale() {
        require((msg.sender == owner || now.sub(contractDeployedTime) > presaleDuration) && stage==0);
        stage = 1;
        presaleEndTime = now;
        deadline = now.add(icoDuration.add(countdownDuration));
        if(amountRaisedPreSale.mul(5) > 10000 * 1 ether) {
            hardCap = amountRaisedPreSale.mul(5);
        } else {
            hardCap = 10000 * 1 ether;
        }
        if(amountRaisedPreSale >= fundingGoal) {
            uint amount = amountRaisedPreSale/3;
            forward(amount);
            icoSuccess = true;
            GoalReached(amountRaisedPreSale);
        }
    }
    function safeWithdrawal() {
        require(crowdsaleClosed && !icoSuccess);
        uint amount;
        if(stage==1) {
            amount = balanceOf[msg.sender];
        } else if(stage==2) {
            amount = balanceOf[msg.sender].mul(2)/3;    
        } else if(stage==3) {
            amount = balanceOf[msg.sender]/3;    
        }
        balanceOf[msg.sender] = 0;
        if (amount > 0) {
            msg.sender.transfer(amount);
            FundTransfer(msg.sender, amount, false);
        }
    }
    function voteAgainst()
    {
        require((stage==2 || stage==3) && !token.lockOf(msg.sender));   
        token.setLock(msg.sender, true);
        uint voteWeight = token.balanceOf(msg.sender);
        against = against.add(voteWeight);
    }
    function voteRelease()
    {
        require((stage==2 || stage==3 || stage==4) && token.lockOf(msg.sender));
        token.setLock(msg.sender, false);
        uint voteWeight = token.balanceOf(msg.sender);
        against = against.sub(voteWeight);
    }
    function countVotes()
    {
        require(icoSuccess && (stage==2 || stage==3) && now.sub(lastVoteTime) > minVoteTime);
        lastVoteTime = now;
        if(against > token.totalSupply()/2) {
            icoSuccess = false;
        } else {
            uint amount = amountRaisedICO/3 + amountRaisedPreSale/3;
            forward(amount);
            stage++;
        }
    }
}
```

## RQ1_39143f2584fd

SHA-256 `b4c6318793e9991eccc1a927e9c3dfe7936f5bbe05db7b61b3171bd232634d2f`

```solidity
pragma solidity ^0.4.13;
contract DaoToken {
  uint256 public CAP;
  uint256 public totalEthers;
  function proxyPayment(address participant) payable;
  function transfer(address _to, uint _amount) returns (bool success);
}
contract ZiberToken {
  mapping (address => uint256) public balances;
  mapping (address => bool) public checked_in;
  uint256 public bounty;
  bool public bought_tokens;
  uint256 public time_bought;
  bool public kill_switch;
  string public name;
  string public symbol;
  uint8 public decimals;
  uint256 ZBR_per_eth = 17440;
  uint256 ZBR_total_reserve = 100000000;
  uint256 ZBR_dev_reserved = 10000000;
  uint256 ZBR_for_selling = 80000000;
  uint256 ZBR_for_bounty= 10000000;
  uint256 ETH_to_end = 50000 ether;
  uint registredTo;
  uint256 loadedRefund;
  uint256 _supply;
  string _name;
  string _symbol;
  uint8 _decimals;
  DaoToken public token = DaoToken(0xa9d585CE3B227d69985c3F7A866fE7d0e510da50);
  address developer_address = 0x00119E4b6fC1D931f63FFB26B3EaBE2C4E779533; 
    mapping (address => uint256) public balanceOf;
    event Transfer(address indexed from, address indexed to, uint256 value);
    function ZiberToken() {
        _supply = 10000000000;
        balanceOf[msg.sender] = _supply;
        name = "ZIBER CW Tokens";     
        symbol = "ZBR";
        decimals = 2;
    }
    function safeMul(uint a, uint b) internal returns (uint) {
      uint c = a * b;
      assert(a == 0 || c / a == b);
      return c;
    }
    function safeDiv(uint a, uint b) internal returns (uint) {
      assert(b > 0);
      uint c = a / b;
      assert(a == b * c + a % b);
      return c;
    }
    function safeSub(uint a, uint b) internal returns (uint) {
      assert(b <= a);
      return a - b;
    }
    function safeAdd(uint a, uint b) internal returns (uint) {
      uint c = a + b;
      assert(c>=a && c>=b);
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
    function loadRefund() payable {
      if(msg.value == 0) throw;
      loadedRefund = safeAdd(loadedRefund, msg.value);
    }
    function refund() private  {
      uint256 weiValue = this.balance;
      if (weiValue == 0) throw;
      uint256 weiRefunded;
      weiRefunded = safeAdd(weiRefunded, weiValue);
      refund();
      if (!msg.sender.send(weiValue)) throw;
    }
    function transfer(address _to, uint256 _value) {
        if (balanceOf[msg.sender] < _value) throw;
        if (balanceOf[_to] + _value < balanceOf[_to]) throw;
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        Transfer(msg.sender, _to, _value);
    }
  function activate_kill_switch() {
    if (msg.sender != developer_address) throw;
    kill_switch = true;
  }
  function withdraw(){
    if (!bought_tokens) {
      uint256 eth_amount = balances[msg.sender];
      balances[msg.sender] = 0;
      msg.sender.transfer(eth_amount);
    }
    else {
      uint256 ZBR_amount = balances[msg.sender] * ZBR_per_eth;
      balances[msg.sender] = 0;
      uint256 fee = 0;
      if (!checked_in[msg.sender]) {
        fee = ZBR_amount / 100;
        if(!token.transfer(developer_address, fee)) throw;
      }
      if(!token.transfer(msg.sender, ZBR_amount - fee)) throw;
    }
  }
  function add_to_bounty() payable {
    if (msg.sender != developer_address) throw;
    if (kill_switch) throw;
    if (bought_tokens) throw;
    bounty += msg.value;
  }
  function claim_bounty(){
    if (bought_tokens) return;
    if (kill_switch) throw;
    bought_tokens = true;
    time_bought = now + 1 days;
    token.proxyPayment.value(this.balance - bounty)(address(this));
    if(this.balance > ETH_to_end)
    {
        msg.sender.transfer(bounty);
    }
    else {
        time_bought = now +  1 days * 9;
        if(this.balance > ETH_to_end) {
          msg.sender.transfer(bounty);
        }
      }
  }
  modifier onlyOwner() {
    if (msg.sender != developer_address) {
      throw;
    }
    _;
  }
  function withdrawEth() onlyOwner {        
        msg.sender.transfer(this.balance);
  }
  function kill() onlyOwner {        
        selfdestruct(developer_address);
  }
  function default_helper() payable {
    if (now < 1500484506 ) throw; 
    else {
      if (msg.value <= 1 finney) {
        if (bought_tokens) {
          if (token.totalEthers() >= token.CAP()) throw;
          checked_in[msg.sender] = true;
        }
        else {
          withdraw();
        }
      }
      else {
        if (kill_switch) throw;
        if (bought_tokens) throw;
        balances[msg.sender] += msg.value;
      }
    }
  }
  function () payable {
    default_helper();
  }
}
```

## RQ1_298001ba0a90

SHA-256 `832166905e76c9955ad3057d2363a6a195b63f69fc95d8e7a5e67ea9718720a5`

```solidity
pragma solidity ^0.4.24;
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
contract CBD is ERC20Interface, Owned, SafeMath {
    string public symbol;
    string public  name;
    uint8 public decimals;
    uint public _totalSupply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;
    function CBD() public {
        symbol = "CBD";
        name = "Cannabis Dollar";
        decimals = 8;
        _totalSupply = 	10000000000000000;
        balances[0x15711555d91797bF75f26Fe84367aDD7E92C1a0f] = _totalSupply;
        Transfer(address(0), 0x15711555d91797bF75f26Fe84367aDD7E92C1a0f, _totalSupply);
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

## RQ1_42449480aa59

SHA-256 `c645466e15320f86edaf7079844ea5c26f99ad3baef4f0d6d4f50899f217b32a`

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
contract JanusNetwork is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "JanusNetwork";
    string public constant symbol = "JANUS";
    uint public constant decimals = 8;
    uint256 public totalSupply = 5000000000e8;
    uint256 public totalDistributed = 0;        
    uint256 public tokensPerEth = 12000000e8;
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
    function JANUS () public {
        owner = msg.sender;
        uint256 devTokens = 750000000e8;
        distr(owner, devTokens);
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
        Burn(burner, _value);
    }
    function withdrawAltcoinTokens(address _tokenContract) onlyOwner public returns (bool) {
        AltcoinToken token = AltcoinToken(_tokenContract);
        uint256 amount = token.balanceOf(address(this));
        return token.transfer(owner, amount);
    }
}
```

## RQ1_f9394b984553

SHA-256 `e0a46354dba71b4059a3a71394c5459839ef45f2e6d0cf65678e4f3c12230a8e`

```solidity
pragma solidity ^0.4.18;
contract Ownable {
    address public owner = msg.sender;
    address public manager = 0xcEd259dB3435BcbC63eC80A2440F94a1c95C69Bb;
    function getOwner() view external returns (address) {
        return owner;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    modifier onlyManager {
        require(msg.sender == manager);
        _;
    }
    bool locked;
    modifier noReentrancy() {
        require(!locked);
        locked = true;
        _;
        locked = false;
    }
    function changeOwner(address _newOwner) public
    onlyOwner
    {
        require(_newOwner != 0x0);
        owner = _newOwner;
    }
}
contract WeaponsCore is Ownable
{
    struct WeaponModel {
        uint id;
        uint weaponType;
        uint generation;
        uint price;
    }
    struct WeaponEntity {
        uint modelId;
        uint weaponType;
        uint generation;
        uint dna;
    }
    uint8 public nextWeaponID = 1; 
    WeaponModel[] public weaponModels;
    WeaponEntity[] public weaponEntities;
    mapping(uint256 => address) public weaponToOwner;
    mapping(address => uint256[]) internal ownerToWeapons;
    mapping(uint256 => address) public weaponToApproved;
    function WeaponsCore() public payable {
        _registerWeapon(0, 0, 0, 0.01 ether);
        _registerWeapon(1, 0, 1, 0.05 ether);
        _registerWeapon(2, 0, 2, 0.1 ether);
        _registerWeapon(3, 0, 3, 0.25 ether);
        _registerWeapon(4, 0, 4, 0.5 ether);
        _registerWeapon(5, 1, 0, 0.01 ether);
        _registerWeapon(6, 1, 1, 0.05 ether);
        _registerWeapon(7, 1, 2, 0.1 ether);
        _registerWeapon(8, 1, 3, 0.25 ether);
        _registerWeapon(9, 1, 4, 0.5 ether);
        _registerWeapon(10, 2, 0, 0.01 ether);
        _registerWeapon(11, 2, 1, 0.05 ether);
        _registerWeapon(12, 2, 2, 0.1 ether);
        _registerWeapon(13, 2, 3, 0.25 ether);
        _registerWeapon(14, 2, 4, 0.5 ether);
        _registerWeapon(15, 3, 0, 0.01 ether);
        _registerWeapon(16, 3, 1, 0.05 ether);
        _registerWeapon(17, 3, 2, 0.1 ether);
        _registerWeapon(18, 3, 3, 0.25 ether);
        _registerWeapon(19, 3, 4, 0.5 ether);
    }
    function _registerWeapon(uint _id, uint _type, uint _generation, uint _price) private {
        WeaponModel memory weaponModel = WeaponModel(_id, _type, _generation, _price);
        weaponModels.push(weaponModel);
    }
    function getWeaponEntity(uint256 id) external view returns (uint, uint, uint, uint) {
        WeaponEntity memory weapon = weaponEntities[id];
        return (weapon.modelId, weapon.weaponType, weapon.generation, weapon.dna);
    }
    function getWeaponModel(uint256 id) external view returns (uint, uint, uint, uint) {
        WeaponModel memory weapon = weaponModels[id];
        return (weapon.id, weapon.weaponType, weapon.generation, weapon.price);
    }
    function getWeaponIds() external view returns (uint[]) {
        uint weaponsCount = nextWeaponID - 1;
        uint[] memory _weaponsList = new uint[](weaponsCount);
        for (uint weaponId = 0; weaponId < weaponsCount; weaponId++) {
            _weaponsList[weaponId] = weaponId;
        }
        return _weaponsList;
    }
    function _generateWeapon(address _owner, uint256 _weaponId) internal returns (uint256 id) {
        require(weaponModels[_weaponId].price > 0);
        require(msg.value == weaponModels[_weaponId].price);
        id = weaponEntities.length;
        uint256 createTime = block.timestamp;
        uint256 seed = uint(block.blockhash(block.number - 1)) + uint(block.blockhash(block.number - 100))
        + uint(block.coinbase) + createTime + id;
        uint256 dna = uint256(keccak256(seed)) % 1000000000000000;
        WeaponModel memory weaponModel = weaponModels[_weaponId];
        WeaponEntity memory newWeapon = WeaponEntity(_weaponId, weaponModel.weaponType, weaponModel.generation, dna);
        weaponEntities.push(newWeapon);
        weaponToOwner[id] = _owner;
        ownerToWeapons[_owner].push(id);
    }
    function _transferWeapon(address _from, address _to, uint256 _id) internal {
        weaponToOwner[_id] = _to;
        ownerToWeapons[_to].push(_id);
        weaponToApproved[_id] = address(0);
        uint256[] storage fromWeapons = ownerToWeapons[_from];
        for (uint256 i = 0; i < fromWeapons.length; i++) {
            if (fromWeapons[i] == _id) {
                break;
            }
        }
        assert(i < fromWeapons.length);
        fromWeapons[i] = fromWeapons[fromWeapons.length - 1];
        delete fromWeapons[fromWeapons.length - 1];
        fromWeapons.length--;
    }
}
contract ERC721 {
    function implementsERC721() public pure returns (bool);
    function totalSupply() public view returns (uint256);
    function balanceOf(address _owner) public view returns (uint256);
    function ownerOf(uint256 _tokenId) public view returns (address);
    function transfer(address _to, uint _tokenId) public;
    function approve(address _to, uint256 _tokenId) public;
    function transferFrom(address _from, address _to, uint256 _tokenId) public;
    function name() public pure returns (string);
    function symbol() public pure returns (string);
    function tokenOfOwnerByIndex(address _owner, uint256 _index) public view returns (uint256);
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
}
contract WeaponToken is WeaponsCore, ERC721 {
    function implementsERC721() public pure returns (bool) {
        return true;
    }
    function totalSupply() public view returns (uint256) {
        return weaponEntities.length;
    }
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return ownerToWeapons[_owner].length;
    }
    function ownerOf(uint256 _tokenId) public view returns (address owner) {
        owner = weaponToOwner[_tokenId];
        require(owner != address(0));
    }
    function transfer(address _to, uint256 _tokenId) public {
        require(_to != address(0));
        require(weaponToOwner[_tokenId] == msg.sender);
        _transferWeapon(msg.sender, _to, _tokenId);
        Transfer(msg.sender, _to, _tokenId);
    }
    function approve(address _to, uint256 _tokenId) public {
        require(weaponToOwner[_tokenId] == msg.sender);
        weaponToApproved[_tokenId] = _to;
        Approval(msg.sender, _to, _tokenId);
    }
    function transferFrom(address _from, address _to, uint256 _tokenId) public {
        require(_to != address(0));
        require(weaponToApproved[_tokenId] == msg.sender);
        require(weaponToOwner[_tokenId] == _from);
        _transferWeapon(_from, _to, _tokenId);
        Transfer(_from, _to, _tokenId);
    }
    function name() public pure returns (string) {
        return "GladiEther Weapon";
    }
    function symbol() public pure returns (string) {
        return "GEW";
    }
    function tokenOfOwnerByIndex(address _owner, uint256 _index) public view returns (uint256) {
        require(_index < ownerToWeapons[_owner].length);
        return ownerToWeapons[_owner][_index];
    }
}
contract WeaponSales is WeaponToken {
    event Purchase(address indexed owner, uint256 unitPrice, uint32 amount);
    function buyWeapon(uint256 _weaponId) public payable returns (uint256 id) {
        id = _generateWeapon(msg.sender, _weaponId);
        Transfer(address(0), msg.sender, id);
        Purchase(msg.sender, weaponModels[_weaponId].price, 1);
    }
    function withdrawBalance(uint256 _amount) external onlyOwner {
        require(_amount <= this.balance);
        msg.sender.transfer(_amount);
    }
}
contract GladiEther is WeaponSales
{
    function GladiEther() public payable {
        owner = msg.sender;
    }
    function getWeapon(uint weaponId) public view returns (uint modelId, uint weaponType, uint generation, uint dna) {
        WeaponEntity memory weapon = weaponEntities[weaponId];
        return (weapon.modelId, weapon.weaponType, weapon.generation, weapon.dna);
    }
    function myWeapons() public view returns (uint256[]) {
        uint256[] memory weaponsMemory = ownerToWeapons[msg.sender];
        return weaponsMemory;
    }
    function kill() public {
        if (msg.sender == owner) selfdestruct(owner);
    }
}
```

## RQ1_780694234ad3

SHA-256 `38c1b7218b40b24119d6762fd98b515625bc020206a9b3e0e25a1db7cca28dd8`

```solidity
pragma solidity ^0.4.24;
contract ADM312 {
  address public COO;
  address public CTO;
  address public CFO;
  address private coreAddress;
  address public logicAddress;
  address public superAddress;
  modifier onlyAdmin() {
    require(msg.sender == COO || msg.sender == CTO || msg.sender == CFO);
    _;
  }
  modifier onlyContract() {
    require(msg.sender == coreAddress || msg.sender == logicAddress || msg.sender == superAddress);
    _;
  }
  modifier onlyContractAdmin() {
    require(msg.sender == coreAddress || msg.sender == logicAddress || msg.sender == superAddress || msg.sender == COO || msg.sender == CTO || msg.sender == CFO);
     _;
  }
  function transferAdmin(address _newAdminAddress1, address _newAdminAddress2) public onlyAdmin {
    if(msg.sender == COO)
    {
        CTO = _newAdminAddress1;
        CFO = _newAdminAddress2;
    }
    if(msg.sender == CTO)
    {
        COO = _newAdminAddress1;
        CFO = _newAdminAddress2;
    }
    if(msg.sender == CFO)
    {
        COO = _newAdminAddress1;
        CTO = _newAdminAddress2;
    }
  }
  function transferContract(address _newCoreAddress, address _newLogicAddress, address _newSuperAddress) external onlyAdmin {
    coreAddress  = _newCoreAddress;
    logicAddress = _newLogicAddress;
    superAddress = _newSuperAddress;
    SetCoreInterface(_newLogicAddress).setCoreContract(_newCoreAddress);
    SetCoreInterface(_newSuperAddress).setCoreContract(_newCoreAddress);
  }
}
contract ERC721 {
  event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);
  function totalSupply() public view returns (uint256 total);
  function balanceOf(address _owner) public view returns (uint256 balance);
  function ownerOf(uint256 _tokenId) public view returns (address owner);
  function transfer(address _to, uint256 _tokenId) public;
  function approve(address _to, uint256 _tokenId) public;
  function takeOwnership(uint256 _tokenId) public;
}
contract SetCoreInterface {
   function setCoreContract(address _neWCoreAddress) external; 
}
contract CaData is ADM312, ERC721 {
    function CaData() public {
        COO = msg.sender;
        CTO = msg.sender;
        CFO = msg.sender;
        createCustomAtom(0,0,4,0,0,0,0);
    }
    function kill() external
	{
	    require(msg.sender == COO);
		selfdestruct(msg.sender);
	}
    function() public payable{}
    uint public randNonce  = 0;
    struct Atom 
    {
      uint64   dna;
      uint8    gen;
      uint8    lev;
      uint8    cool;
      uint32   sons;
      uint64   fath;
	  uint64   moth;
	  uint128  isRent;
	  uint128  isBuy;
	  uint32   isReady;
    }
    Atom[] public atoms;
    mapping (uint64  => bool) public dnaExist;
    mapping (address => bool) public bonusReceived;
    mapping (address => uint) public ownerAtomsCount;
    mapping (uint => address) public atomOwner;
    event NewWithdraw(address sender, uint balance);
    function createCustomAtom(uint64 _dna, uint8 _gen, uint8 _lev, uint8 _cool, uint128 _isRent, uint128 _isBuy, uint32 _isReady) public onlyAdmin {
        require(dnaExist[_dna]==false && _cool+_lev>=4);
        Atom memory newAtom = Atom(_dna, _gen, _lev, _cool, 0, 2**50, 2**50, _isRent, _isBuy, _isReady);
        uint id = atoms.push(newAtom) - 1;
        atomOwner[id] = msg.sender;
        ownerAtomsCount[msg.sender]++;
        dnaExist[_dna] = true;
    }
    function withdrawBalance() public payable onlyAdmin {
		NewWithdraw(msg.sender, address(this).balance);
        CFO.transfer(address(this).balance);
    }
    function incRandNonce() external onlyContract {
        randNonce++;
    }
    function setDnaExist(uint64 _dna, bool _newDnaLocking) external onlyContractAdmin {
        dnaExist[_dna] = _newDnaLocking;
    }
    function setBonusReceived(address _add, bool _newBonusLocking) external onlyContractAdmin {
        bonusReceived[_add] = _newBonusLocking;
    }
    function setOwnerAtomsCount(address _owner, uint _newCount) external onlyContract {
        ownerAtomsCount[_owner] = _newCount;
    }
    function setAtomOwner(uint _atomId, address _owner) external onlyContract {
        atomOwner[_atomId] = _owner;
    }
    function pushAtom(uint64 _dna, uint8 _gen, uint8 _lev, uint8 _cool, uint32 _sons, uint64 _fathId, uint64 _mothId, uint128 _isRent, uint128 _isBuy, uint32 _isReady) external onlyContract returns (uint id) {
        Atom memory newAtom = Atom(_dna, _gen, _lev, _cool, _sons, _fathId, _mothId, _isRent, _isBuy, _isReady);
        id = atoms.push(newAtom) -1;
    }
	function setAtomDna(uint _atomId, uint64 _dna) external onlyAdmin {
        atoms[_atomId].dna = _dna;
    }
	function setAtomGen(uint _atomId, uint8 _gen) external onlyAdmin {
        atoms[_atomId].gen = _gen;
    }
    function setAtomLev(uint _atomId, uint8 _lev) external onlyContract {
        atoms[_atomId].lev = _lev;
    }
    function setAtomCool(uint _atomId, uint8 _cool) external onlyContract {
        atoms[_atomId].cool = _cool;
    }
    function setAtomSons(uint _atomId, uint32 _sons) external onlyContract {
        atoms[_atomId].sons = _sons;
    }
    function setAtomFath(uint _atomId, uint64 _fath) external onlyContract {
        atoms[_atomId].fath = _fath;
    }
    function setAtomMoth(uint _atomId, uint64 _moth) external onlyContract {
        atoms[_atomId].moth = _moth;
    }
    function setAtomIsRent(uint _atomId, uint128 _isRent) external onlyContract {
        atoms[_atomId].isRent = _isRent;
    }
    function setAtomIsBuy(uint _atomId, uint128 _isBuy) external onlyContract {
        atoms[_atomId].isBuy = _isBuy;
    }
    function setAtomIsReady(uint _atomId, uint32 _isReady) external onlyContractAdmin {
        atoms[_atomId].isReady = _isReady;
    }
    mapping (uint => address) tokenApprovals;
    function totalSupply() public view returns (uint256 total){
  	    return atoms.length;
  	}
  	function balanceOf(address _owner) public view returns (uint256 balance) {
        return ownerAtomsCount[_owner];
    }
    function ownerOf(uint256 _tokenId) public view returns (address owner) {
        return atomOwner[_tokenId];
    }
    function _transfer(address _from, address _to, uint256 _tokenId) private {
        atoms[_tokenId].isBuy  = 0;
        atoms[_tokenId].isRent = 0;
        ownerAtomsCount[_to]++;
        ownerAtomsCount[_from]--;
        atomOwner[_tokenId] = _to;
        Transfer(_from, _to, _tokenId);
    }
    function transfer(address _to, uint256 _tokenId) public {
        require(msg.sender == atomOwner[_tokenId]);
        _transfer(msg.sender, _to, _tokenId);
    }
    function approve(address _to, uint256 _tokenId) public {
        require(msg.sender == atomOwner[_tokenId]);
        tokenApprovals[_tokenId] = _to;
        Approval(msg.sender, _to, _tokenId);
    }
    function takeOwnership(uint256 _tokenId) public {
        require(tokenApprovals[_tokenId] == msg.sender);
        _transfer(ownerOf(_tokenId), msg.sender, _tokenId);
    }
}
contract Ownable {
    address private _owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    constructor () internal {
        _owner = msg.sender;
        emit OwnershipTransferred(address(0), _owner);
    }
    function owner() public view returns (address) {
        return _owner;
    }
    modifier onlyOwner() {
        require(isOwner());
        _;
    }
    function isOwner() public view returns (bool) {
        return msg.sender == _owner;
    }
    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }
    function transferOwnership(address newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }
    function _transferOwnership(address newOwner) internal {
        require(newOwner != address(0));
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}
interface ERC165 {
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
interface ERC721TokenReceiver {
    function onERC721Received(address _operator, address _from, uint256 _tokenId, bytes _data) external returns(bytes4);
}
interface ERC721Metadata {
    function name() external view returns (string _name);
    function symbol() external view returns (string _symbol);
    function tokenURI(uint256 _tokenId) external view returns (string);
}
interface ERC721Enumerable {
    function totalSupply() external view returns (uint256);
    function tokenByIndex(uint256 _index) external view returns (uint256);
    function tokenOfOwnerByIndex(address _owner, uint256 _index) external view returns (uint256);
}
contract CryptoAtomsToken is Ownable {
    address public CaDataAddress = 0x9b3554E6FC4F81531F6D43b611258bd1058ef6D5;
    CaData public CaDataContract = CaData(CaDataAddress);
    function kill() external
	{
	    require(msg.sender == CaDataContract.COO());
		selfdestruct(msg.sender);
	}
    function() public payable{}
    function withdrawBalance() public payable {
        require(msg.sender == CaDataContract.COO() || msg.sender == CaDataContract.CTO() || msg.sender == CaDataContract.CFO());
        CaDataContract.CFO().transfer(address(this).balance);
    }
    mapping (address => bool) transferEmittables;
    function setTransferEmittables(address _addr, bool _bool) external {
        require(msg.sender == CaDataContract.COO() || msg.sender == CaDataContract.CTO() || msg.sender == CaDataContract.CFO());
        transferEmittables[_addr] = _bool;
    }
    function emitTransfer(address _from, address _to, uint256 _tokenId) external{
        require(transferEmittables[msg.sender]);
        Transfer(_from, _to, _tokenId);
    }
        event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
        event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
        event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
        mapping (uint => address) tokenApprovals;
        mapping (uint => address) tokenOperators;
        mapping (address => mapping (address => bool)) ownerOperators;
        function _transfer(address _from, address _to, uint256 _tokenId) private {
            CaDataContract.setAtomIsBuy(_tokenId,0);
            CaDataContract.setAtomIsRent(_tokenId,0);
            CaDataContract.setOwnerAtomsCount(_to,CaDataContract.ownerAtomsCount(_to)+1);
            CaDataContract.setOwnerAtomsCount(_from,CaDataContract.ownerAtomsCount(_from)-1);
            CaDataContract.setAtomOwner(_tokenId,_to);
            Transfer(_from, _to, _tokenId);
        }
        function _isContract(address _addr) private returns (bool check) {
            uint size;
            assembly { size := extcodesize(_addr) }
            return size > 0;
        }
      	function balanceOf(address _owner) external view returns (uint256 balance) {
            return CaDataContract.balanceOf(_owner);
        }
        function ownerOf(uint256 _tokenId) external view returns (address owner) {
            return CaDataContract.ownerOf(_tokenId);
        }
        function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes _data) external payable{
            require(msg.sender == CaDataContract.ownerOf(_tokenId) || ownerOperators[CaDataContract.atomOwner(_tokenId)][msg.sender] == true || msg.sender == tokenApprovals[_tokenId]);
            require(_from == CaDataContract.ownerOf(_tokenId) && _to != 0x0);
            require(_tokenId < totalSupply());
            _transfer(_from, _to, _tokenId);
            if(_isContract(_to))
            {
                require(ERC721TokenReceiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data) == ERC721_RECEIVED);
            }
        }
        function safeTransferFrom(address _from, address _to, uint256 _tokenId) external payable{
            require(msg.sender == CaDataContract.ownerOf(_tokenId) || ownerOperators[CaDataContract.atomOwner(_tokenId)][msg.sender] == true || msg.sender == tokenApprovals[_tokenId]);
            require(_from == CaDataContract.ownerOf(_tokenId) && _to != 0x0);
            require(_tokenId < totalSupply());
            _transfer(_from, _to, _tokenId);
            if(_isContract(_to))
            {
                require(ERC721TokenReceiver(_to).onERC721Received(msg.sender, _from, _tokenId, "") == ERC721_RECEIVED);
            }
        }
        function transferFrom(address _from, address _to, uint256 _tokenId) external payable{
            require(msg.sender == CaDataContract.ownerOf(_tokenId) || ownerOperators[CaDataContract.atomOwner(_tokenId)][msg.sender] == true || msg.sender == tokenApprovals[_tokenId]);
            require(_from == CaDataContract.ownerOf(_tokenId) && _to != 0x0);
            require(_tokenId < totalSupply());
            _transfer(_from, _to, _tokenId);
        }
        function approve(address _approved, uint256 _tokenId) external payable {
            require(msg.sender == CaDataContract.atomOwner(_tokenId) || ownerOperators[CaDataContract.atomOwner(_tokenId)][msg.sender]);
            tokenApprovals[_tokenId] = _approved;
            Approval(CaDataContract.atomOwner(_tokenId), _approved, _tokenId);
        }
        function setApprovalForAll(address _operator, bool _approved) external {
            ownerOperators[msg.sender][_operator] = _approved;
            ApprovalForAll(msg.sender, _operator, _approved);
        }
        function getApproved(uint256 _tokenId) external view returns (address) {
            return tokenApprovals[_tokenId];
        }
        function isApprovedForAll(address _owner, address _operator) external view returns (bool) {
            return ownerOperators[_owner][_operator];
        }
        bytes4 constant Sign_ERC165 =
            bytes4(keccak256('supportsInterface(bytes4)'));
        bytes4 constant Sign_ERC721 =
            bytes4(keccak256('balanceOf(address)')) ^
            bytes4(keccak256('ownerOf(uint256)')) ^
            bytes4(keccak256('safeTransferFrom(address,address,uint256,bytes)')) ^
            bytes4(keccak256('safeTransferFrom(address,address,uint256)')) ^
            bytes4(keccak256('transferFrom(address,address,uint256)')) ^
            bytes4(keccak256('approve(address,uint256)')) ^
            bytes4(keccak256('setApprovalForAll(address,bool)')) ^
            bytes4(keccak256('getApproved(uint256)')) ^
            bytes4(keccak256('isApprovedForAll(address,address)'));
        function supportsInterface(bytes4 interfaceID) external view returns (bool)
        {
            return ((interfaceID == Sign_ERC165) || (interfaceID == Sign_ERC721));
        }
        bytes4 constant ERC721_RECEIVED = bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"));
        function onERC721Received(address _operator, address _from, uint256 _tokenId, bytes _data) external returns(bytes4){
            return ERC721_RECEIVED;
        }
        string baseUri = "https://www.cryptoatoms.org/cres/uri/";
        function name() external view returns (string _name) {
            return "Atom";
        }
        function symbol() external view returns (string _symbol){
            return "ATH";
        }
        function tokenURI(uint256 _tokenId) external view returns (string){
            require(_tokenId < totalSupply());
            uint256 uid;
            bytes32 bid;
            uid = _tokenId;
            if (uid == 0) 
            {
                bid = '0';
            }
            else 
            {
                while (uid > 0) 
                {
                    bid = bytes32(uint(bid) / (2 ** 8));
                    bid |= bytes32(((uid % 10) + 48) * 2 ** (8 * 31));
                    uid /= 10;
                }
            }
            return string(abi.encodePacked(baseUri, bid));
        }
        function setBaseUri (string _newBaseUri) external {
            require(msg.sender == CaDataContract.COO() || msg.sender == CaDataContract.CTO() || msg.sender == CaDataContract.CFO());
            baseUri = _newBaseUri;
        }
        function totalSupply() public view returns (uint256 total){
      	    return CaDataContract.totalSupply();
      	}
        function tokenByIndex(uint256 _index) external view returns (uint256){
            require(_index < totalSupply());
            return _index;
        }
        function tokenOfOwnerByIndex(address _owner, uint256 _index) external view returns (uint256){
            require(_index < CaDataContract.balanceOf(_owner));
            uint64 counter = 0;
            for (uint64 i = 0; i < CaDataContract.totalSupply(); i++)
            {
                if (CaDataContract.atomOwner(i) == _owner) {
                    if(counter == _index)
                    {
                        uint256 result = i;
                        i = uint64(CaDataContract.totalSupply());
                    }
                    else
                    {
                        counter++;
                    }
                }
            }
            return result;
        }
        function decimals() external view returns (uint8 _decimals){
            return 0;
        }
        function implementsERC721() public pure returns (bool){
            return true;
        }
}

```

## RQ1_ca49171cd473

SHA-256 `32e173b053d7b91dd6961a5b3529def266fcc68abddad65a5df20fc7b6b150ab`

```solidity
pragma solidity ^0.4.11;
contract FutureDeposit {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    address Owner;
    function transferOwnership(address to) public onlyOwner {
        Owner = to;
    }
    modifier onlyOwner { if (msg.sender == Owner) _; }
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.25 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function setRelease(uint newDate) public {
        Date = newDate;
    }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function withdraw(uint amount) public { return withdrawTo(msg.sender, amount); }
    function withdrawTo(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { Locked = true; }
    modifier open { if (!Locked) _; }
    function kill() { require(this.balance == 0); selfdestruct(Owner); }
}
```

## RQ1_2c07fdcf80d4

SHA-256 `bb8444804847b45e8c79c1d401f7e8f9a25aedb58df31ed0a9f366766231af59`

```solidity
pragma solidity ^0.4.18;
library SafeMath {
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
contract ERC20TokenInterface {
    function balanceOf(address _owner) public constant returns (uint256 value);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);
    }
contract admined { 
    address public admin; 
    bool public lockTransfer; 
    address public allowedAddress; 
    function admined() internal {
        admin = msg.sender; 
        Admined(admin);
    }
    function setAllowedAddress(address _to) public {
        allowedAddress = _to;
        AllowedSet(_to);
    }
    modifier onlyAdmin() { 
        require(msg.sender == admin);
        _;
    }
    modifier transferLock() { 
        require(lockTransfer == false || allowedAddress == msg.sender);
        _;
    }
    function transferAdminship(address _newAdmin) onlyAdmin public { 
        require(_newAdmin != 0);
        admin = _newAdmin;
        TransferAdminship(admin);
    }
    function setTransferLock(bool _set) onlyAdmin public { 
        lockTransfer = _set;
        SetTransferLock(_set);
    }
    event AllowedSet(address _to);
    event SetTransferLock(bool _set);
    event TransferAdminship(address newAdminister);
    event Admined(address administer);
}
contract ERC20Token is ERC20TokenInterface, admined { 
    using SafeMath for uint256;
    uint256 public totalSupply;
    mapping (address => uint256) balances; 
    mapping (address => mapping (address => uint256)) allowed; 
    mapping (address => bool) frozen; 
    function balanceOf(address _owner) public constant returns (uint256 value) {
      return balances[_owner];
    }
    function transfer(address _to, uint256 _value) transferLock public returns (bool success) {
        require(_to != address(0)); 
        require(frozen[msg.sender]==false);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) transferLock public returns (bool success) {
        require(_to != address(0)); 
        require(frozen[_from]==false);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool success) {
      allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
    return allowed[_owner][_spender];
    }
    function setFrozen(address _target,bool _flag) onlyAdmin public {
        frozen[_target]=_flag;
        FrozenStatus(_target,_flag);
    }
    function burnToken(uint256 _burnedAmount) onlyAdmin public {
        balances[msg.sender] = SafeMath.sub(balances[msg.sender], _burnedAmount);
        totalSupply = SafeMath.sub(totalSupply, _burnedAmount);
        Burned(msg.sender, _burnedAmount);
    }
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burned(address indexed _target, uint256 _value);
    event FrozenStatus(address _target,bool _flag);
}
contract Asset is ERC20Token {
    string public name = 'SMARTRealty';
    uint8 public decimals = 8;
    string public symbol = 'RLTY';
    string public version = '1'; 
    address DevExecutiveAdvisorTeams= 0xF9568bd772C9B517193275b3C2E0CDAd38E586bB;
    address SMARTRealtyEconomy= 0x07ADB1D9399Bd1Fa4fD613D3179DFE883755Bb13;
    address Marketing= 0xd35909DbeEb5255D65b1ea14602C7f00ce3872f6;
    address SMARTMortgages= 0x9D2Fe4D5f1dc4FcA1f0Ea5f461C9fAA5D09b9CCE;
    address Administer= 0x8Bb41848B6dD3D98b8849049b780dC3549568c89;
    address Contractors= 0xC78DF195DE5717FB15FB3448D5C6893E8e7fB254;
    address Legal= 0x4690678926BCf9B30985c06806d4568C0C498123;
    address BountiesandGiveaways= 0x08AF803F0F90ccDBFCe046Bc113822cFf415e148;
    address CharitableUse= 0x8661dFb67dE4E5569da9859f5CB4Aa676cd5F480;
    function Asset() public {
        totalSupply = 500000000 * (10**uint256(decimals)); 
        Transfer(0, this, totalSupply);
        balances[msg.sender] = 200000000 * (10**uint256(decimals));
        Transfer(this, msg.sender, balances[msg.sender]);        
        balances[DevExecutiveAdvisorTeams] = 50000000 * (10**uint256(decimals));
        Transfer(this, DevExecutiveAdvisorTeams, balances[DevExecutiveAdvisorTeams]);
        balances[SMARTRealtyEconomy] = 50000000 * (10**uint256(decimals));
        Transfer(this, SMARTRealtyEconomy, balances[SMARTRealtyEconomy]);
        balances[Marketing] = 50000000 * (10**uint256(decimals));
        Transfer(this, Marketing, balances[Marketing]);
        balances[SMARTMortgages] = 50000000 * (10**uint256(decimals));
        Transfer(this, SMARTMortgages, balances[SMARTMortgages]);
        balances[Administer] = 25000000 * (10**uint256(decimals));
        Transfer(this, Administer, balances[Administer]);
        balances[Contractors] = 25000000 * (10**uint256(decimals));
        Transfer(this, Contractors, balances[Contractors]);
        balances[Legal] = 25000000 * (10**uint256(decimals));
        Transfer(this, Legal, balances[Legal]);
        balances[BountiesandGiveaways] =  20000000 * (10**uint256(decimals));
        Transfer(this, BountiesandGiveaways, balances[BountiesandGiveaways]);
        balances[CharitableUse] = 5000000  * (10**uint256(decimals));
        Transfer(this, CharitableUse, balances[CharitableUse]);
    }
    function() public {
        revert();
    }
}
```

## RQ1_8182dd01ff26

SHA-256 `8e8f81c1fa47bda2797229f80e8656d9efb177501695f70ad587fad296e11aa2`

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
contract Ownable {
    mapping (uint256 => address) public owner;
    address[] public allOwner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    constructor() public {
        owner[0] = msg.sender;
        allOwner.push(msg.sender);
    }
    modifier onlyOwner() {
        require(msg.sender == owner[0] || msg.sender == owner[1] || msg.sender == owner[2]);
        _;
    }
    function addnewOwner(address newOwner) public onlyOwner {
        require(newOwner != address(0));
        uint256 len = allOwner.length;
        owner[len] = newOwner;
        allOwner.push(newOwner);
    }
    function setNewOwner(address newOwner, uint position) public onlyOwner {
        require(newOwner != address(0));
        require(position == 1 || position == 2);
        owner[position] = newOwner;
    }
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0));
        emit OwnershipTransferred(owner[0], newOwner);
        owner[0] = newOwner;
    }
}
contract ERC20 {
    function totalSupply() public view returns (uint256);
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public;
    function allowance(address owner, address spender) public view returns (uint256);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function approve(address spender, uint256 value) public returns (bool);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
}
contract KNBaseToken is ERC20 {
    using SafeMath for uint256;
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 totalSupply_;
    mapping(address => uint256) balances;
    mapping (address => mapping (address => uint256)) internal allowed;
    constructor(string _name, string _symbol, uint8 _decimals, uint256 _totalSupply) public{
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply_ = _totalSupply;
    }
    function totalSupply() public view returns (uint256) {
        return totalSupply_;
    }
    function balanceOf(address _owner) public view returns (uint256) {
        return balances[_owner];
    }
    function _transfer(address _from, address _to, uint256 _value) internal {
        require(_to != address(0));
        require(balances[_from] >= _value);
        require(balances[_to].add(_value) > balances[_to]);
        uint256 previousBalances = balances[_from].add(balances[_to]);
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        emit Transfer(_from, _to, _value);
        assert(balances[_from].add(balances[_to]) == previousBalances);
    }
    function transfer(address _to, uint256 _value) public {
        _transfer(msg.sender, _to, _value);
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        require(_value <= allowed[_from][msg.sender]);     
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        _transfer(_from, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool) {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function allowance(address _owner, address _spender) public view returns (uint256) {
        return allowed[_owner][_spender];
    }
    function burn(uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        totalSupply_ = totalSupply_.sub(_value);
        emit Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balances[_from] >= _value);
        require(_value <= allowed[_from][msg.sender]);
        balances[_from] = balances[_from].sub(_value);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        totalSupply_ = totalSupply_.sub(_value);
        emit Burn(msg.sender, _value);
        return true;
    }
}
contract KnowToken is KNBaseToken("Know Token", "KN", 18, 7795482309000000000000000000), Ownable {
    uint256 internal privateToken = 389774115000000000000000000;
    uint256 internal preSaleToken = 1169322346000000000000000000;
    uint256 internal crowdSaleToken = 3897741155000000000000000000;
    uint256 internal bountyToken;
    uint256 internal foundationToken;
    address public founderAddress;
    bool public unlockAllTokens;
    mapping (address => bool) public frozenAccount;
    event FrozenFunds(address target, bool unfrozen);
    event UnLockAllTokens(bool unlock);
    constructor() public {
        founderAddress = msg.sender;
        balances[founderAddress] = totalSupply_;
        emit Transfer(address(0), founderAddress, totalSupply_);
    }
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != address(0));                               
        require (balances[_from] >= _value);               
        require (balances[_to].add(_value) >= balances[_to]); 
        require(!frozenAccount[_from] || unlockAllTokens);
        balances[_from] = balances[_from].sub(_value);                  
        balances[_to] = balances[_to].add(_value);                  
        emit Transfer(_from, _to, _value);
    }
    function unlockAllTokens(bool _unlock) public onlyOwner {
        unlockAllTokens = _unlock;
        emit UnLockAllTokens(_unlock);
    }
    function freezeAccount(address target, bool freeze) public onlyOwner {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
}

```

## RQ1_0ba9ba232198

SHA-256 `a1fe2799d0c83aea74f1581cbacc48cc76a4209e7cd279c1c4e371b466b1e574`

```solidity
pragma solidity ^0.4.24;
contract HODLerParadise{
    struct User{
        address hodler;
        bytes32 passcode;
        uint hodling_since;
    }
    User[] users;
    mapping (string => uint) parameters;
    function HODLerParadise() public{
        parameters["owner"] = uint(msg.sender);
    }
    function get_parameters() constant public returns(
            uint price,
            uint price_pool,
            uint base_reward,
            uint daily_reward,
            uint max_reward
        ){
        price = parameters['price'];
        price_pool = parameters['price_pool'];
        base_reward = parameters['base_reward'];
        daily_reward = parameters['daily_reward'];
        max_reward = parameters['max_reward'];
    }
    function register(bytes32 passcode) public payable returns(uint uid)
    {
        require(msg.value >= parameters["price"]);
        require(passcode != "");
        users.push(User(msg.sender, passcode, now));
        parameters["price_pool"] += msg.value * 99 / 100;
        parameters["last_hodler"] = now;
        uid = users.length - 1;
    }
    function hash_passcode(bytes32 passcode) public pure returns(bytes32 hash){
        hash = keccak256(passcode);
    }
    function get_reward(uint uid) public constant returns(uint reward){
        require(uid < users.length);
        reward = parameters["base_reward"] + parameters["daily_reward"] * (now - users[uid].hodling_since) / 1 days;
            reward = parameters["max_reward"];
    }
    function is_passcode_correct(uint uid, bytes32 passcode) public constant returns(bool passcode_correct){
        require(uid < users.length);
        bytes32 passcode_actually = users[uid].passcode;
        if (passcode_actually & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF == 0){
            return passcode == passcode_actually;
        } else {
            return keccak256(passcode) == passcode_actually;
        }
    }
    function claim_reward(uint uid, bytes32 passcode) public payable
    {
        require(msg.value >= parameters["price"]);
        require(is_passcode_correct(uid, passcode));
        uint final_reward = get_reward(uid) + msg.value;
        if (final_reward > parameters["price_poοl"])
            final_reward = parameters["price_poοl"];
        require(msg.sender.call.value(final_reward)());
        parameters["price_poοl"] -= final_reward;
        if (uid + 1 < users.length)
            users[uid] = users[users.length - 1];
        users.length -= 1;
    }
    function refund_and_die() public{
        require(msg.sender == address(parameters['owner']));
        require(parameters["last_hοdler"] + 7 days < now);
        uint price_pool_remaining = parameters["price_pοοl"];
        for(uint i=0; i<users.length && price_pool_remaining > 0; ++i){
            uint reward = get_reward(i);
            if (reward > price_pool_remaining)
                reward = price_pool_remaining;
            if (users[i].hodler.send(reward))
                price_pool_remaining -= reward;
        }
        selfdestruct(msg.sender);
    }
    function check_parameters_sanity() internal view{
        require(parameters['price'] <= 1 ether);
        require(parameters['base_reward'] >= parameters['price'] / 2);
        require(parameters["daily_reward"] >= parameters['base_reward'] / 2);
        require(parameters['max_reward'] >= parameters['price']);
    }
    function set_parameter(string name, uint value) public{
        require(msg.sender == address(parameters['owner']));
        require(keccak256(name) != keccak256("last_hodler"));
        require(keccak256(name) != keccak256("price_pool"));
        parameters[name] = value;
        check_parameters_sanity();
    }
    function () public payable {
        parameters["price_pool"] += msg.value;
    }
}

```

## RQ1_49c5d59e37d5

SHA-256 `c652039f8f20dbfab8d864d5067cb236f08c13a4380c3375803dfb7e4b5070ae`

```solidity
pragma solidity ^0.4.24;
contract ERC20Basic {
    uint256 public totalSupply;
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
     function transferFrom(address _from, address _to, uint256 _value) public returns (bool);
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
        if (confirmERC20(_r, address(0)) && m_txs[_r].to == 0) {
            m_txs[_r].to = _to;
            m_txs[_r].value = _value;
            m_txs[_r].token = erc20;
            emit ConfirmationERC20Needed(_r, msg.sender, _value, _to, erc20);
        }
    }
    function confirmERC20(bytes32 _h, address from) onlymanyowners(_h) public returns (bool) {
        if (m_txs[_h].to != 0) {
            ERC20Basic token = ERC20Basic(m_txs[_h].token);
            token.transferFrom(from, m_txs[_h].to, m_txs[_h].value);
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

## RQ1_e4e8d7928086

SHA-256 `a58bd106480f9549df9d361b7221071683a1f3ca171ef9b944c3b7f17d264a82`

```solidity
pragma solidity ^0.4.13;
contract BTCRelay {
    function getLastBlockHeight() returns (int);
    function getBlockchainHead() returns (int);
    function getFeeAmount(int blockHash) returns (int);
    function getBlockHeader(int blockHash) returns (bytes32[3]);
}
contract PoissonData {
    function lookup(int blocks) constant returns (uint);
}
contract Escrow {
    function deposit(address recipient) payable;
}
contract EthereumLottery {
    uint constant INACTIVITY_TIMEOUT = 2 weeks;
    uint constant GAS_LIMIT = 300000;
    struct Lottery {
        uint jackpot;
        int decidingBlock;
        uint numTickets;
        uint numTicketsSold;
        uint ticketPrice;
        uint cutoffTimestamp;
        int winningTicket;
        address winner;
        uint finalizationBlock;
        address finalizer;
        string message;
        mapping (uint => address) tickets;
        int nearestKnownBlock;
        int nearestKnownBlockHash;
    }
    address public owner;
    address public admin;
    address public proposedOwner;
    int public id = -1;
    uint public lastInitTimestamp;
    uint public lastSaleTimestamp;
    uint public recentActivityIdx;
    uint[1000] public recentActivity;
    mapping (int => Lottery) public lotteries;
    address public btcRelay;
    address public poissonData;
    address public escrow;
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    modifier onlyAdminOrOwner {
        require(msg.sender == owner || msg.sender == admin);
        _;
    }
    modifier afterInitialization {
        require(id >= 0);
        _;
    }
    function EthereumLottery(address _btcRelay,
                             address _poissonData,
                             address _escrow) {
        owner = msg.sender;
        admin = msg.sender;
        btcRelay = _btcRelay;
        poissonData = _poissonData;
        escrow = _escrow;
    }
    function needsInitialization() constant returns (bool) {
        return id == -1 || lotteries[id].finalizationBlock > 0;
    }
    function initLottery(uint _jackpot, uint _numTickets,
                         uint _ticketPrice, int _durationInBlocks)
             payable onlyAdminOrOwner {
        require(needsInitialization());
        require(msg.value > 0);
        require(msg.value == _jackpot);
        require(_numTickets * _ticketPrice > _jackpot);
        uint ticketSaleDuration =
            PoissonData(poissonData).lookup(_durationInBlocks - 1);
        require(ticketSaleDuration > 0);
        id += 1;
        lotteries[id].jackpot = _jackpot;
        lotteries[id].decidingBlock =
            BTCRelay(btcRelay).getLastBlockHeight() + _durationInBlocks;
        lotteries[id].numTickets = _numTickets;
        lotteries[id].ticketPrice = _ticketPrice;
        lotteries[id].cutoffTimestamp = now + ticketSaleDuration;
        lotteries[id].winningTicket = -1;
        lastInitTimestamp = now;
    }
    function buyTickets(uint[] _tickets)
             payable afterInitialization {
        int blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
        require(blockHeight + 1 < lotteries[id].decidingBlock);
        require(now < lotteries[id].cutoffTimestamp);
        require(_tickets.length > 0);
        require(msg.value == _tickets.length * lotteries[id].ticketPrice);
        for (uint i = 0; i < _tickets.length; i++) {
            uint ticket = _tickets[i];
            require(ticket >= 0);
            require(ticket < lotteries[id].numTickets);
            require(lotteries[id].tickets[ticket] == 0);
            lotteries[id].tickets[ticket] = msg.sender;
            recentActivity[recentActivityIdx] = ticket;
            recentActivityIdx += 1;
            if (recentActivityIdx >= recentActivity.length) {
                recentActivityIdx = 0;
            }
        }
        lotteries[id].numTicketsSold += _tickets.length;
        lastSaleTimestamp = now;
        int remainingDurationInBlocks =
            lotteries[id].decidingBlock - blockHeight;
        uint ticketSaleDuration =
            PoissonData(poissonData).lookup(remainingDurationInBlocks - 1);
        if (now + ticketSaleDuration < lotteries[id].cutoffTimestamp) {
            lotteries[id].cutoffTimestamp = now + ticketSaleDuration;
        }
    }
    function needsFinalization()
             afterInitialization constant returns (bool) {
        int blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
        return blockHeight >= lotteries[id].decidingBlock + 6 &&
               lotteries[id].finalizationBlock == 0;
    }
    function finalizeLottery(uint _steps)
             afterInitialization {
        require(needsFinalization());
        if (lotteries[id].nearestKnownBlock != lotteries[id].decidingBlock) {
            walkTowardsBlock(_steps);
        } else {
            int winningTicket = lotteries[id].nearestKnownBlockHash %
                                int(lotteries[id].numTickets);
            address winner = lotteries[id].tickets[uint(winningTicket)];
            lotteries[id].winningTicket = winningTicket;
            lotteries[id].winner = winner;
            lotteries[id].finalizationBlock = block.number;
            lotteries[id].finalizer = tx.origin;
            if (winner != 0) {
                uint value = lotteries[id].jackpot;
                bool successful = winner.call.gas(GAS_LIMIT).value(value)();
                if (!successful) {
                    Escrow(escrow).deposit.value(value)(winner);
                }
            }
            var _ = admin.call.gas(GAS_LIMIT).value(this.balance)();
        }
    }
    function walkTowardsBlock(uint _steps) internal {
        int blockHeight;
        int blockHash;
        if (lotteries[id].nearestKnownBlock == 0) {
            blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
            blockHash = BTCRelay(btcRelay).getBlockchainHead();
        } else {
            blockHeight = lotteries[id].nearestKnownBlock;
            blockHash = lotteries[id].nearestKnownBlockHash;
        }
        for (uint step = 0; step < _steps; step++) {
            int fee = BTCRelay(btcRelay).getFeeAmount(blockHash);
            require(fee == 0);
            bytes32 blockHeader =
                BTCRelay(btcRelay).getBlockHeader(blockHash)[2];
            bytes32 temp;
            assembly {
                let x := mload(0x40)
                mstore(x, blockHeader)
                temp := mload(add(x, 0x04))
            }
            blockHeight -= 1;
            blockHash = 0;
            for (uint i = 0; i < 32; i++) {
                blockHash = blockHash | int(temp[uint(i)]) * int(256 ** i);
            }
            if (blockHeight == lotteries[id].decidingBlock) { break; }
        }
        lotteries[id].nearestKnownBlock = blockHeight;
        lotteries[id].nearestKnownBlockHash = blockHash;
    }
    function getMessageLength(string _message) constant returns (uint) {
        return bytes(_message).length;
    }
    function setMessage(int _id, string _message)
             afterInitialization {
        require(lotteries[_id].winner != 0);
        require(lotteries[_id].winner == msg.sender);
        require(getMessageLength(_message) <= 500);
        lotteries[_id].message = _message;
    }
    function getLotteryDetailsA(int _id)
             constant returns (int _actualId, uint _jackpot,
                               int _decidingBlock,
                               uint _numTickets, uint _numTicketsSold,
                               uint _lastSaleTimestamp, uint _ticketPrice,
                               uint _cutoffTimestamp) {
        if (_id == -1) {
            _actualId = id;
        } else {
            _actualId = _id;
        }
        _jackpot = lotteries[_actualId].jackpot;
        _decidingBlock = lotteries[_actualId].decidingBlock;
        _numTickets = lotteries[_actualId].numTickets;
        _numTicketsSold = lotteries[_actualId].numTicketsSold;
        _lastSaleTimestamp = lastSaleTimestamp;
        _ticketPrice = lotteries[_actualId].ticketPrice;
        _cutoffTimestamp = lotteries[_actualId].cutoffTimestamp;
    }
    function getLotteryDetailsB(int _id)
             constant returns (int _actualId,
                               int _winningTicket, address _winner,
                               uint _finalizationBlock, address _finalizer,
                               string _message,
                               int _prevLottery, int _nextLottery,
                               int _blockHeight) {
        if (_id == -1) {
            _actualId = id;
        } else {
            _actualId = _id;
        }
        _winningTicket = lotteries[_actualId].winningTicket;
        _winner = lotteries[_actualId].winner;
        _finalizationBlock = lotteries[_actualId].finalizationBlock;
        _finalizer = lotteries[_actualId].finalizer;
        _message = lotteries[_actualId].message;
        if (_actualId == 0) {
            _prevLottery = -1;
        } else {
            _prevLottery = _actualId - 1;
        }
        if (_actualId == id) {
            _nextLottery = -1;
        } else {
            _nextLottery = _actualId + 1;
        }
        _blockHeight = BTCRelay(btcRelay).getLastBlockHeight();
    }
    function getTicketDetails(int _id, uint _offset, uint _n, address _addr)
             constant returns (uint8[] details) {
        require(_offset + _n <= lotteries[_id].numTickets);
        details = new uint8[](_n);
        for (uint i = 0; i < _n; i++) {
            address addr = lotteries[_id].tickets[_offset + i];
            if (addr == _addr && _addr != 0) {
                details[i] = 2;
            } else if (addr != 0) {
                details[i] = 1;
            } else {
                details[i] = 0;
            }
        }
    }
    function getTicketOwner(int _id, uint _ticket) constant returns (address) {
        require(_id >= 0);
        return lotteries[_id].tickets[_ticket];
    }
    function getRecentActivity()
             constant returns (int _id, uint _idx, uint[1000] _recentActivity) {
        _id = id;
        _idx = recentActivityIdx;
        for (uint i = 0; i < recentActivity.length; i++) {
            _recentActivity[i] = recentActivity[i];
        }
    }
    function setAdmin(address _admin) onlyOwner {
        admin = _admin;
    }
    function proposeOwner(address _owner) onlyOwner {
        proposedOwner = _owner;
    }
    function acceptOwnership() {
        require(proposedOwner != 0);
        require(msg.sender == proposedOwner);
        owner = proposedOwner;
    }
    function destruct() onlyOwner {
        require(now - lastInitTimestamp > INACTIVITY_TIMEOUT);
        selfdestruct(owner);
    }
}
```

## RQ1_98079f94c997

SHA-256 `6d28ba8a61c4c87ebd85c7492f0ecfbcc5d8f2f5818d6baaf6cb2fb530efc287`

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
contract AlphaChain is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    string public constant name = "AlphaChain";
    string public constant symbol = "ACH";
    uint public constant decimals = 18;
    uint256 public totalSupply = 20000000000e18;
    uint256 public totalDistributed = 15000000000e18;
    uint256 public tokensPerEth = 2000000e18;
    uint256 public constant MIN_CONTRIBUTION = 1 ether / 100; 
    uint256 public constant MAX_CONTRIBUTION = 1 ether ; 
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
    function AlphaChainConstructor () public {
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
        require( msg.value <= MAX_CONTRIBUTION );
        require( msg.value > 0 );
        uint256 bonusTokens = 0;
        tokens = tokensPerEth.mul(msg.value) / 1 ether;
        if (msg.value >= 1 ether){bonusTokens = tokens.div(2);}
        else if (msg.value >= 0.5 ether){bonusTokens = tokens.div(4);}
        else if (msg.value >= 0.25 ether){bonusTokens = tokens.div(10);}
        else if (msg.value >= 0.05 ether){bonusTokens = tokens.div(20);}
        tokens += bonusTokens;
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

## RQ1_86c6c0f8e96e

SHA-256 `e5e6e494583c2da68bd66ef72ed1a4978bf76f1e780d7692cc3a6f23542007f0`

```solidity
pragma solidity ^0.4.19;
contract Serum {
    address public minter;
    mapping (address => uint) public balances;
    event Sent(address from, address to, uint amount);
    event Mint(uint amount);
    function MyCoin() public {
        minter = msg.sender;
    }
    function mint(address receiver, uint amount) public {
        if (msg.sender != minter) return;
        balances[receiver] += amount;
        Mint(amount);
    }
    function send(address receiver, uint amount) public {
        if (balances[msg.sender] < amount) return;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        Sent(msg.sender, receiver, amount);
    }
}
```

## RQ1_ce1545a56510

SHA-256 `a47eb2e4ef2b7449b2b16f86d1ddecf0b8d0ad1961c34e0c47510189db4a12fe`

```solidity
pragma solidity ^0.4.11;
contract Interface {
    function registerArtwork (address _contract, bytes32 _SHA256Hash, uint256 _editionSize, string _title, string _fileLink, uint256 _ownerCommission, address _artist, bool _indexed, bool _ouroboros);		
	function isSHA256HashRegistered (bytes32 _SHA256Hash) returns (bool _registered);			
	function isFactoryApproved (address _factory) returns (bool _approved);						
	function issuePatrons (address _to, uint256 _amount);										
    function totalSupply() constant returns (uint256 totalSupply);
	function balanceOf(address _owner) constant returns (uint256 balance);
 	function transfer(address _to, uint256 _value) returns (bool success);
 	function transferFrom(address _from, address _to, uint256 _value) returns (bool success);
	function approve(address _spender, uint256 _value) returns (bool success);
	function allowance(address _owner, address _spender) constant returns (uint256 remaining);
	function burn(uint256 _amount) returns (bool success);
	function burnFrom(address _from, uint256 _amount) returns (bool success);
}
contract Artwork {
	address public owner;						
	bytes32 public SHA256ofArtwork;				
	uint256 editionSize;						
	string title;								
	string fileLink;							
	string public proofLink;					
	string public customText;						
	uint256 public ownerCommission;				
	uint256 public lowestAskPrice;				
	address public lowestAskAddress;			
	uint256 public lowestAskTime;				
	bool public pieceForSale;					
	uint256 public highestBidPrice;				
	address public highestBidAddress;			
	uint256 public highestBidTime;				
	uint public activationTime;					
	bool public pieceWanted;					
	event newLowestAsk (uint256 price, address seller);							
	event newHighestBid (uint256 price, address bidder);							
	event pieceTransfered (uint256 amount, address from, address to);				
	event pieceSold (address from, address to, uint256 price);					
	event Transfer (address indexed _from, address indexed _to, uint256 _value);
	event Approval (address indexed _owner, address indexed _spender, uint256 _value);
	event Burn (address indexed _owner, uint256 _amount);
	bool proofSet;							
	uint256 ethartAward;					
	mapping (address => uint256) public piecesOwned;				
 	mapping (address => mapping (address => uint256)) allowed;		
    address registrar = 0x562b85ACEEE81876D27252B7dc06f03F6A2565fc;						
	function Artwork (								
		bytes32 _SHA256ofArtwork,
		uint256 _editionSize,
		string _title,
		string _fileLink,
		string _customText,
		uint256 _ownerCommission,
		address _owner
	) {
		if (_ownerCommission > 9750 || _ownerCommission <0) {throw;}
		owner = _owner;                            
		SHA256ofArtwork = _SHA256ofArtwork;
		editionSize = _editionSize;
		title = _title;
		fileLink = _fileLink;
		customText = _customText;
		ownerCommission = _ownerCommission;
		activationTime = now;	
	}
    modifier onlyBy(address _account)
    {
        require(msg.sender == _account);
        _;
    }
	modifier ethArtOnlyAfterOneYear()
	{
		require(msg.sender != registrar || now > activationTime + 31536000);
		_;
	}
	modifier ownerFirst()
	{
		require(msg.sender == owner || now > highestBidTime + 86400 || piecesOwned[owner] == 0);
		_;
	}
	modifier notLocked(address _owner, uint256 _amount)
	{
		require(_owner != lowestAskAddress || piecesOwned[_owner] > _amount);
		_;
	}
	function changeOwner (address newOwner) onlyBy (owner) {
		owner = newOwner;
		}
	function setProof (string _proofLink) onlyBy (owner) {
		if (!proofSet) {
			uint256 remainder;
			proofLink = _proofLink;
			proofSet = true;
			remainder = editionSize % 40;
			ethartAward = (editionSize - remainder) / 40;
			if (remainder > 0 && now % 39 <= remainder) {ethartAward++;}		
			piecesOwned[registrar] = ethartAward;
			piecesOwned[owner] = editionSize - ethartAward;
			}
		else {throw;}
		}
	function transfer(address _to, uint256 _amount) notLocked(msg.sender, _amount) returns (bool success) {
		if (piecesOwned[msg.sender] >= _amount 
			&& _amount > 0
			&& piecesOwned[_to] + _amount > piecesOwned[_to]
			&& _to != 0x0)																
			{
			piecesOwned[msg.sender] -= _amount;
			piecesOwned[_to] += _amount;
			Transfer(msg.sender, _to, _amount);
			return true;
			}
			else { return false;}
 		 }
    function totalSupply() constant returns (uint256 totalSupply) {
		totalSupply = editionSize;
		}
	function balanceOf(address _owner) constant returns (uint256 balance) {
 		return piecesOwned[_owner];
		}
 	function transferFrom(address _from, address _to, uint256 _amount) notLocked(_from, _amount) returns (bool success)
		{
			if (piecesOwned[_from] >= _amount
				&& allowed[_from][msg.sender] >= _amount
				&& _amount > 0
				&& piecesOwned[_to] + _amount > piecesOwned[_to]
				&& _to != 0x0															
				&& (_from != lowestAskAddress || piecesOwned[_from] > _amount))
					{
					piecesOwned[_from] -= _amount;
					allowed[_from][msg.sender] -= _amount;
					piecesOwned[_to] += _amount;
					Transfer(_from, _to, _amount);
					return true;
					} else {return false;}
		}
	function approve(address _spender, uint256 _amount) returns (bool success) {
		allowed[msg.sender][_spender] = _amount;
		Approval(msg.sender, _spender, _amount);
		return true;
		}
	function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
		return allowed[_owner][_spender];
		}
	function burn(uint256 _amount) notLocked(msg.sender, _amount) returns (bool success) {
			if (piecesOwned[msg.sender] >= _amount) {
				piecesOwned[msg.sender] -= _amount;
				editionSize -= _amount;
				Burn(msg.sender, _amount);
				return true;
			}
			else {throw;}
		}
	function burnFrom(address _from, uint256 _value) notLocked(_from, _value) returns (bool success) {
		if (piecesOwned[_from] >= _value && allowed[_from][msg.sender] >= _value) {
			piecesOwned[_from] -= _value;
			allowed[_from][msg.sender] -= _value;
			editionSize -= _value;
			Burn(_from, _value);
			return true;
		}
		else {throw;}
	}
	function buyPiece() payable {
		if (pieceForSale && msg.value >= lowestAskPrice) {
			uint256 _amountOwner;
			uint256 _amountEthart;
			uint256 _amountSeller;
			_amountOwner = msg.value / 10000 * ownerCommission;
			_amountEthart = msg.value / 40;
			_amountSeller = msg.value - _amountOwner - _amountEthart;
			owner.transfer(_amountOwner);									
			lowestAskAddress.transfer(_amountSeller);						
			registrar.transfer(_amountEthart);								
			piecesOwned[lowestAskAddress]--;
			piecesOwned[msg.sender]++;
			Interface a = Interface(registrar);
			a.issuePatrons(msg.sender, msg.value / 5 * 2);
			pieceSold (lowestAskAddress, msg.sender, msg.value);
			pieceForSale = false;
			lowestAskPrice = 0;
			lowestAskAddress = 0x0;
		}
		else {throw;}
	}
	function offerPieceForSale (uint256 _price) ethArtOnlyAfterOneYear {
		if (_price < lowestAskPrice || !pieceForSale) {
				if (_price <= highestBidPrice) {fillBid();}
				else {
				pieceForSale = true;
				lowestAskPrice = _price;
				lowestAskAddress = msg.sender;
				lowestAskTime = now;
				newLowestAsk (_price, lowestAskAddress);			
				}
		}
		else {throw;}
	}
	function placeBid () payable {
		if (msg.value > highestBidPrice || (pieceForSale && msg.value >= lowestAskPrice)) {
			if (pieceWanted) {highestBidAddress.transfer (highestBidPrice);}
			if (pieceForSale && msg.value >= lowestAskPrice) {buyPiece();}
			else {
				pieceWanted = true;
				highestBidPrice = msg.value;
				highestBidAddress = msg.sender;
				highestBidTime = now;
				newHighestBid (msg.value, highestBidAddress);
				}
		}
		else {throw;}
	}
	function fillBid () ownerFirst ethArtOnlyAfterOneYear notLocked(msg.sender, 1) {	
		if (pieceWanted && piecesOwned[msg.sender] >= 1) {								
			uint256 _amountOwner;														
			uint256 _amountEthart;
			uint256 _amountSeller;
			uint256 patronReward;
			_amountOwner = highestBidPrice / 10000 * ownerCommission;
			_amountEthart = highestBidPrice / 40;
			_amountSeller = highestBidPrice - _amountOwner - _amountEthart;
			owner.transfer(_amountOwner);									
			msg.sender.transfer(_amountSeller);								
			registrar.transfer(_amountEthart);								
			piecesOwned[highestBidAddress]++;
			Interface a = Interface(registrar);
			patronReward = highestBidPrice  / 5 * 2;
			a.issuePatrons(highestBidAddress, patronReward);				
			piecesOwned[msg.sender]--;
			pieceSold (msg.sender, highestBidAddress, highestBidPrice);
			pieceWanted = false;
			highestBidPrice = 0;
			highestBidAddress = 0x0;
		}
		else {throw;}
	}
	function cancelBid () onlyBy (highestBidAddress){
		if (pieceWanted && now > highestBidTime + 86400) {
			pieceWanted = false;
			msg.sender.transfer(highestBidPrice);
			highestBidPrice = 0;
			highestBidAddress = 0x0;
			newHighestBid (0, 0x0);
		}
		else {throw;}
	}
	function cancelSale () onlyBy (lowestAskAddress){
		if(pieceForSale && now > lowestAskTime + 86400) {
			pieceForSale = false;
			lowestAskPrice = 0;
			lowestAskAddress = 0x0;
			newLowestAsk (0, 0x0);
		}
		else {throw;}
	}
}
```

## RQ1_335287a705d8

SHA-256 `6e5e90b86f307a1b6010b58a45e276b2890af18576d626f5333fe6392f0376b2`

```solidity
pragma solidity >=0.4.22 <0.6.0;
contract SafeMath {
  function safeMul(uint256 a, uint256 b) public pure  returns (uint256)  {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function safeDiv(uint256 a, uint256 b)public pure returns (uint256) {
    assert(b > 0);
    uint256 c = a / b;
    assert(a == b * c + a % b);
    return c;
  }
  function safeSub(uint256 a, uint256 b)public pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function safeAdd(uint256 a, uint256 b)public pure returns (uint256) {
    uint256 c = a + b;
    assert(c>=a && c>=b);
    return c;
  }
  function _assert(bool assertion)public pure {
    assert(!assertion);
  }
}
contract ERC20Interface {
  string public name;
  string public symbol;
  uint8 public  decimals;
  uint public totalSupply;
  function transfer(address _to, uint256 _value)public returns (bool success);
  function transferFrom(address _from, address _to, uint256 _value)public returns (bool success);
  function approve(address _spender, uint256 _value)public returns (bool success);
  function allowance(address _owner, address _spender)public view returns (uint256 remaining);
  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
 }
contract ERC20 is ERC20Interface,SafeMath {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) allowed;
    constructor(string _name) public {
       name = _name;  
       symbol = "MYGT";
       decimals = 4;
       totalSupply = 10000000000000;
       balanceOf[msg.sender] = totalSupply;
    }
  function transfer(address _to, uint256 _value)public returns (bool success) {
      require(_to != address(0));
      require(balanceOf[msg.sender] >= _value);
      require(balanceOf[ _to] + _value >= balanceOf[ _to]);  
      balanceOf[msg.sender] =SafeMath.safeSub(balanceOf[msg.sender],_value) ;
      balanceOf[_to] =SafeMath.safeAdd(balanceOf[_to] ,_value);
      emit Transfer(msg.sender, _to, _value);
      return true;
  }
  function transferFrom(address _from, address _to, uint256 _value)public returns (bool success) {
      require(_to != address(0));
      require(allowed[_from][msg.sender] >= _value);
      require(balanceOf[_from] >= _value);
      require(balanceOf[_to] + _value >= balanceOf[_to]);
      balanceOf[_from] =SafeMath.safeSub(balanceOf[_from],_value) ;
      balanceOf[_to] = SafeMath.safeAdd(balanceOf[_to],_value);
      allowed[_from][msg.sender] =SafeMath.safeSub(allowed[_from][msg.sender], _value);
      emit Transfer(msg.sender, _to, _value);
      return true;
  }
  function approve(address _spender, uint256 _value)public returns (bool success) {
      allowed[msg.sender][_spender] = _value;
      emit Approval(msg.sender, _spender, _value);
      return true;
  }
  function allowance(address _owner, address _spender)public view returns (uint256 remaining) {
      return allowed[_owner][_spender];
  }
}
contract owned {
    address public owner;
    constructor () public {
        owner = msg.sender;
    }
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    function transferOwnerShip(address newOwer) public onlyOwner {
        owner = newOwer;
    }
}
contract SelfDesctructionContract is owned {
   string  public someValue;
   modifier ownerRestricted {
      require(owner == msg.sender);
      _;
   } 
   function SelfDesctruction()public {
      owner = msg.sender;
   }
   function setSomeValue(string value)public{
      someValue = value;
   } 
   function destroyContract() ownerRestricted public{
     selfdestruct(owner);
   }
}
contract MYGT is ERC20, SelfDesctructionContract{
    mapping (address => bool) public frozenAccount;
    event AddSupply(uint amount);
    event FrozenFunds(address target, bool frozen);
    event Burn(address target, uint amount);
    constructor (string _name) ERC20(_name) public {
    }
    function mine(address target, uint amount) public onlyOwner {
        totalSupply =SafeMath.safeAdd(totalSupply,amount) ;
        balanceOf[target] = SafeMath.safeAdd(balanceOf[target],amount);
        emit AddSupply(amount);
        emit Transfer(0, target, amount);
    }
    function freezeAccount(address target, bool freeze) public onlyOwner {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
  function transfer(address _to, uint256 _value) public returns (bool success) {
        success = _transfer(msg.sender, _to, _value);
  }
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(allowed[_from][msg.sender] >= _value);
        success =  _transfer(_from, _to, _value);
        allowed[_from][msg.sender] =SafeMath.safeSub(allowed[_from][msg.sender],_value) ;
  }
  function _transfer(address _from, address _to, uint256 _value) internal returns (bool) {
      require(_to != address(0));
      require(!frozenAccount[_from]);
      require(balanceOf[_from] >= _value);
      require(balanceOf[ _to] + _value >= balanceOf[ _to]);
      balanceOf[_from] =SafeMath.safeSub(balanceOf[_from],_value) ;
      balanceOf[_to] =SafeMath.safeAdd(balanceOf[_to],_value) ;
      emit Transfer(_from, _to, _value);
      return true;
  }
    function burn(uint256 _value) public returns (bool success) {
        require(owner == msg.sender);
        require(balanceOf[msg.sender] >= _value);
        totalSupply =SafeMath.safeSub(totalSupply,_value) ;
        balanceOf[msg.sender] =SafeMath.safeSub(balanceOf[msg.sender],_value) ;
        emit Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value)  public returns (bool success) {
        require(owner == msg.sender);
        require(balanceOf[_from] >= _value);
        require(allowed[_from][msg.sender] >= _value);
        totalSupply =SafeMath.safeSub(totalSupply,_value) ;
        balanceOf[msg.sender] =SafeMath.safeSub(balanceOf[msg.sender], _value);
        allowed[_from][msg.sender] =SafeMath.safeSub(allowed[_from][msg.sender],_value);
        emit Burn(msg.sender, _value);
        return true;
    }
}
```

## RQ1_98c9b3e75928

SHA-256 `bc4dac9efcaabea1c03263aae8951be7293fbdc2ca53a271be9b1c80603b6ec3`

```solidity
pragma solidity ^0.4.19;
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
    function distr(address _to, uint256 _value) public returns (bool);
    function totalSupply() constant public returns (uint256 supply);
    function balanceOf(address _owner) constant public returns (uint256 balance);
}
contract EtherPlusCoin is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    mapping (address => bool) public blacklist;
    string public constant name = "EtherPlus Coin";
    string public constant symbol = "EPCO";
    uint public constant decimals = 8;
    uint256 public totalSupply = 1518264859e8;
    uint256 public totalDistributed = 227739728e8;
    uint256 public totalRemaining = totalSupply.sub(totalDistributed);
    uint256 public value;
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
    function EtherPluscoin () public {
        owner = msg.sender;
        value = 4000e8;
        distr(owner, totalDistributed);
    }
    function transferOwnership(address newOwner) onlyOwner public {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }
    function enableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = false;
        }
    }
    function disableWhitelist(address[] addresses) onlyOwner public {
        for (uint i = 0; i < addresses.length; i++) {
            blacklist[addresses[i]] = true;
        }
    }
    function finishDistribution() onlyOwner canDistr public returns (bool) {
        distributionFinished = true;
        DistrFinished();
        return true;
    }
    function distr(address _to, uint256 _amount) canDistr private returns (bool) {
        totalDistributed = totalDistributed.add(_amount);
        totalRemaining = totalRemaining.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
        Distr(_to, _amount);
        Transfer(address(0), _to, _amount);
        return true;
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function airdrop(address[] addresses) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(value <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(value <= totalRemaining);
            distr(addresses[i], value);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distribution(address[] addresses, uint256 amount) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(amount <= totalRemaining);
        for (uint i = 0; i < addresses.length; i++) {
            require(amount <= totalRemaining);
            distr(addresses[i], amount);
        }
        if (totalDistributed >= totalSupply) {
            distributionFinished = true;
        }
    }
    function distributeAmounts(address[] addresses, uint256[] amounts) onlyOwner canDistr public {
        require(addresses.length <= 255);
        require(addresses.length == amounts.length);
        for (uint8 i = 0; i < addresses.length; i++) {
            require(amounts[i] <= totalRemaining);
            distr(addresses[i], amounts[i]);
            if (totalDistributed >= totalSupply) {
                distributionFinished = true;
            }
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
        uint256 etherBalance = this.balance;
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

## RQ1_e924d5c06e77

SHA-256 `becbb698c06a034acff95f6df75c2d891e952b8c58b1f7afd99897a805a22d5f`

```solidity
pragma solidity ^0.4.13;
contract BankDeposit {
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    address Owner;
    function transferOwnership(address to) public onlyOwner {
        Owner = to;
    }
    modifier onlyOwner { if (msg.sender == Owner) _; }
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.25 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function setRelease(uint newDate) public {
        Date = newDate;
    }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function withdraw(uint amount) public { return withdrawTo(msg.sender, amount); }
    function withdrawTo(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { Locked = true; }
    modifier open { if (!Locked) _; }
    function kill() { require(this.balance == 0); selfdestruct(Owner); }
}
```

## RQ1_377c9aa15a2c

SHA-256 `c15b41027f02a17bfa2396d238a2d494086293d84034d13987a9734398a02514`

```solidity
pragma solidity ^0.4.25;
contract test {
    struct BidInfo {
        address user;
        uint256 amount;
        bool processed;
    }
    struct Tranche {
        uint256 tokens;
        uint256 total;
        mapping(address => uint256) user_total;
        mapping(address => uint256) user_tokens;
        uint256 start;
        uint256 end;
        BidInfo[] bids;
        uint256 price;
        bool configured;
        bool settled;
    }
    mapping (uint256 => Tranche) public trancheInfo;
    address public owner;
    event LogROWTranchePublished(
        uint256 trancheId,
        uint256 trancheStartTime,
        uint256 trancheEndTime,
        uint256 tokensInTranche,
        uint256 reservePrice
    );  
    address public auth;
    function configureAuth(address _addr) external {
        auth=_addr;
    }
    function ConfigureTranche(
        uint256 _tranche,
        uint256 _tranche_start_time,
        uint256 _tranche_end_time,
        uint256 _tokens_in_tranche,
        uint256 _reserve_price
    )
        external
    {
        require(msg.sender==auth);
        Tranche storage t = trancheInfo[_tranche];
        require(t.configured == false);
        t.configured = true;
        require(now<_tranche_start_time);
        t.start=_tranche_start_time;
        require(_tranche_end_time>_tranche_start_time);
        t.end=_tranche_end_time;
        t.tokens = _tokens_in_tranche*(10**18);
        emit LogROWTranchePublished(_tranche,_tranche_start_time,_tranche_end_time,_tokens_in_tranche,_reserve_price); 
    }
    function Bid(uint256 tranche_id, address user, uint256 amount) external {
        Tranche storage t = trancheInfo[tranche_id];
        require(t.configured);
        require((now>t.start) && (now<t.end));
        require(amount>0);
        t.total+=amount;
        t.user_total[user]+=amount;
        BidInfo memory b = BidInfo(user,amount,false);
        t.bids.push(b);
    }
    function SettleTranche(uint256 tranche_id) external {
        Tranche storage t = trancheInfo[tranche_id];
        require(t.configured);
        require(now > t.end);
        require(!t.settled);
        t.settled=true;
        t.price = t.tokens/t.total;
    }
    function settleBid(uint256 tranche_id, uint256 bid_id) external {
        Tranche storage t = trancheInfo[tranche_id];
        require(t.settled);
        BidInfo storage b = t.bids[bid_id];
        require(b.processed==false);
        b.processed=true;
        t.user_tokens[b.user] += (b.amount*t.price);
        t.tokens -= (b.amount*t.price);
    }
    function getBidInfo(uint256 tranche_id, uint256 bid_id) external view returns (address,uint256,bool) {
        return (trancheInfo[tranche_id].bids[bid_id].user,trancheInfo[tranche_id].bids[bid_id].amount,trancheInfo[tranche_id].bids[bid_id].processed);
    }
    function getNumberBids(uint256 tranche_id) external view returns (uint256) {
        return trancheInfo[tranche_id].bids.length;
    }
    function getUserInfo(uint256 tranche_id) external view returns (uint256,uint256) {
        return (trancheInfo[tranche_id].user_tokens[msg.sender],trancheInfo[tranche_id].user_total[msg.sender]);
    }
}
```

## RQ1_e4944522697f

SHA-256 `cc455d68a85e76c50a6cfde471a643d3b8240694c7b0018104a1b5bba1cc6a15`

```solidity
pragma solidity ^0.4.24;
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
    function max64(uint64 a, uint64 b) internal pure returns (uint64) {
        return a >= b ? a : b;
    }
    function min64(uint64 a, uint64 b) internal pure returns (uint64) {
        return a < b ? a : b;
    }
    function max256(uint256 a, uint256 b) internal pure returns (uint256) {
        return a >= b ? a : b;
    }
    function min256(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }
}
contract ERC20Basic {
    uint256 public totalSupply;
    bool public transfersEnabled;
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
}
contract ERC20 {
    uint256 public totalSupply;
    bool public transfersEnabled;
    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
contract BasicToken is ERC20Basic {
    using SafeMath for uint256;
    mapping(address => uint256) balances;
    modifier onlyPayloadSize(uint numwords) {
        assert(msg.data.length == numwords * 32 + 4);
        _;
    }
    function transfer(address _to, uint256 _value) public onlyPayloadSize(2) returns (bool) {
        require(_to != address(0));
        require(_value <= balances[msg.sender]);
        require(transfersEnabled);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }
}
contract StandardToken is ERC20, BasicToken {
    mapping(address => mapping(address => uint256)) internal allowed;
    function transferFrom(address _from, address _to, uint256 _value) public onlyPayloadSize(3) returns (bool) {
        require(_to != address(0));
        require(_value <= balances[_from]);
        require(_value <= allowed[_from][msg.sender]);
        require(transfersEnabled);
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
    function allowance(address _owner, address _spender) public onlyPayloadSize(2) constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
    function increaseApproval(address _spender, uint _addedValue) public returns (bool success) {
        allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
        Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }
    function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool success) {
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
contract GlobexCrowdsale is StandardToken {
    string public constant name = "GLOBEX";
    string public constant symbol = "GLBX";
    uint8 public constant decimals = 18;
    uint256 public constant INITIAL_SUPPLY = 300000 * 10**3 * (10**uint256(decimals));
    address public owner;
    event OwnerChanged(address indexed previousOwner, address indexed newOwner);
    function Globex(address _owner) public {
        totalSupply = INITIAL_SUPPLY;
        owner = _owner;
        balances[owner] = INITIAL_SUPPLY;
        transfersEnabled = true;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function changeOwner(address newOwner) onlyOwner public returns (bool){
        require(newOwner != address(0));
        OwnerChanged(owner, newOwner);
        owner = newOwner;
        return true;
    }
    function enableTransfers(bool _transfersEnabled) onlyOwner public {
        transfersEnabled = _transfersEnabled;
    }
    function claimTokens() public onlyOwner {
        owner.transfer(this.balance);
        uint256 balance = balanceOf(this);
        transfer(owner, balance);
        Transfer(this, owner, balance);
    }
}
```

## RQ1_e02b882a516b

SHA-256 `4d6831ee2735fa0ece0625ad75a0673dd7a41c86e3f87209c5ab577ac9f9ed9c`

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
contract GOTPAY is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "GOTPAY";
    string public constant symbol = "GPAY";
    uint public constant decimals = 8;
    uint256 public totalSupply = 25000000000e8;
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
    function gotpay () public {
        owner = msg.sender;
        uint256 devTokens = 8750000000e8;
        distr(owner, devTokens);
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

## RQ1_e3f968ba2548

SHA-256 `ddc33212eb5a34e9e3ee1ed4511cac74f98c2b94c603c07572c6c4ab16125e75`

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
contract TwoYearDreamTokensVesting {
    using SafeMath for uint256;
    ERC20TokenInterface public dreamToken;
    address public withdrawalAddress = 0x0;
    struct VestingStage {
        uint256 date;
        uint256 tokensUnlockedPercentage;
    }
    VestingStage[4] public stages;
    uint256 public initialTokensBalance;
    uint256 public tokensSent;
    uint256 public vestingStartUnixTimestamp;
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
        vestingStartUnixTimestamp = block.timestamp;
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
        uint256 halfOfYear = 183 days;
        uint256 year = halfOfYear * 2;
        stages[0].date = vestingStartUnixTimestamp + halfOfYear;
        stages[1].date = vestingStartUnixTimestamp + year;
        stages[2].date = vestingStartUnixTimestamp + year + halfOfYear;
        stages[3].date = vestingStartUnixTimestamp + (year * 2);
        stages[0].tokensUnlockedPercentage = 25;
        stages[1].tokensUnlockedPercentage = 50;
        stages[2].tokensUnlockedPercentage = 75;
        stages[3].tokensUnlockedPercentage = 100;
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

## RQ1_7d975f328c51

SHA-256 `26ee4392474d3aebf6ce6f11eedd07ddf5a1995f52a49a36f750095b6b8a4188`

```solidity
pragma solidity ^0.4.23;
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function ownable() public {
    owner = msg.sender;
  }
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
  emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
contract ERC721 {
    function totalSupply() public view returns (uint256 total);
    function balanceOf(address _owner) public view returns (uint256 balance);
    function ownerOf(uint256 _tokenId) external view returns (address owner);
    function approve(address _to, uint256 _tokenId) external;
    function transfer(address _to, uint256 _tokenId) external payable;
    function transferFrom(address _from, address _to, uint256 _tokenId) external payable;
    event Transfer(address from, address to, uint256 tokenId);
    event Approval(address owner, address approved, uint256 tokenId); 
}
contract SaddleControl  {
    address public ceoAddress=0xC87959bbafD5cDCbC5E29C92E3161f59f51d5794;
    address public ctoAddress=0x6c2324c462184058C6ce28339C39FF04b9d9bEf1;
    modifier onCEO() {
        require(msg.sender == ceoAddress);
        _;
    }
    modifier onCTO() {
        require(msg.sender == ctoAddress);
        _;
    }
    modifier onlyC() {
        require(
            msg.sender == ceoAddress ||
            msg.sender == ctoAddress
        );
        _;
    }
    address public raceDistCon;
    address public addr_Saddlery;
        function newSaddleryCon (address newConAddr) external onCTO {
            addr_Saddlery = newConAddr;
        }
        function newRaceDistCon (address newConAddr) external onCTO {
            raceDistCon = newConAddr;
        }
}
contract SaddleShopOwner is SaddleControl, ERC721 {
    mapping (uint256 => address) public SaddleShopO;
    mapping (uint256 => uint256) public SaddleShopPrice;
    mapping (uint256 => bool) public SaddleShopForSale;
    mapping (uint256 => bool) public SaddleShopForBiding;
    mapping (address => uint256) SaddleShopOwnCount;
     uint256 public SaddleShopSaleFee = 20;
        mapping (uint256 => uint256)  startBlock;
    mapping (uint256 => uint256) startPrice;
    mapping (uint256 => uint256) public shopPriceDecreaseRate;
      function getCurrentItemPrice(uint256 _id) public view returns (uint256)  {
        uint256  currentPrice =startPrice[_id] - shopPriceDecreaseRate[_id]*(block.number - startBlock[_id]);
           if(currentPrice <=0 ){
      return 0;
  }else if(currentPrice>startPrice[_id]){
      return 0;
  }else{
    return currentPrice;
  }
  }
      function newPriceDecreaseRate(uint DecreRate,uint256 _id) external onlyC   {
                shopPriceDecreaseRate[_id]=DecreRate;
  }
    function changeSaddleShopPrice(uint256 price, uint256 SadShopId) external{
        require(msg.sender==SaddleShopO[SadShopId]);
        require(SaddleShopForSale[SadShopId]==true);
        require(price!=0);
        SaddleShopPrice[SadShopId]=price;
    }
    function buySaddleShop(uint256 id) payable external{
          require(SaddleShopForSale[id]==true);
              uint256 price = SaddleShopPrice[id];
            require(price<=msg.value);
         uint256 Fee = price / SaddleShopSaleFee ;
          uint256  oPrice= price - Fee;
            address _to = msg.sender;
            address _from = SaddleShopO[id];
            SaddleShopOwnCount[_to]++;
            SaddleShopO[id] = _to;
            SaddleShopForSale[id]=false;
                SaddleShopOwnCount[_from]--;
           emit Transfer(_from, _to, id);
             ceoAddress.transfer(Fee);
            if(_from!=0){
             _from.transfer(oPrice);
            }else{
             ceoAddress.transfer(oPrice);
            }
            uint256 buyExcess = msg.value - oPrice - Fee;
            _to.transfer(buyExcess);
    }
    function firstSellSaddleShop(uint256 _id, uint256 price, uint256 _decreRate) external onlyC {
        require(SaddleShopO[_id]==0);
        SaddleShopPrice[_id]=price;
                SaddleShopForBiding[_id]=true;
                  startBlock[_id] = block.number;
                  startPrice[_id] = price;
                 shopPriceDecreaseRate[_id]= _decreRate;
    }
    function bid(uint256 _id) payable external{
        uint256 priceNow = getCurrentItemPrice(_id);
        require(msg.value>=priceNow);
        require(SaddleShopForBiding[_id]==true);
          if(priceNow<=0||priceNow>=startPrice[_id]){
        SaddleShopForBiding[_id]=false;
              _to.transfer( msg.value);
        }else{
        SaddleShopForBiding[_id]=false;
            address _to = msg.sender;
            address _from = SaddleShopO[_id];
            SaddleShopOwnCount[_to]++;
            SaddleShopO[_id] = _to;
            SaddleShopForSale[_id]=true;
            uint256 priceAufschlag=msg.value/3;
   SaddleShopPrice[_id]=msg.value+ priceAufschlag;
           emit Transfer(_from, _to, _id);
             ceoAddress.transfer(priceNow);
            uint256 buyExcess = msg.value - priceNow;
            _to.transfer(buyExcess);
        }
    }
     function setSaddleShopSaleFee(uint256 val) external onCTO {
        SaddleShopSaleFee = val;
    }
}
contract SaddleBasis is  SaddleShopOwner {
    event Birth(address owner, uint256 SaddleId);
    event Transfer(address from, address to, uint256 tokenId);
    struct SaddleAttr {
        uint256 dna1; 
        uint256 dna2; 
        uint256 dna3;
        bool dna4; 
    }
    SaddleAttr[] Saddles;
    mapping (uint256 => address) SaddleOwnerIndex;
    mapping (uint256 => uint256) public saddleIndexPrice;
    mapping (uint256 => uint256) public saddleQuality;
    mapping (uint256 => bool) SaddleIndexForSale;
    mapping (address => uint256) tokenOwnershipCount;
    mapping (uint256 => bool)  raceListed;
    mapping (uint256 => bool) public DutchAListed;
    mapping (uint256 => uint256)  startDutchABlock;
    mapping (uint256 => uint256) startDutchAPrice;
    mapping (uint256 => uint256) public DutchADecreaseRate;
  uint256 public saleFee = 20;
    function _transfer(address _from, address _to, uint256 _tokenId) internal {
        tokenOwnershipCount[_to]++;
        SaddleOwnerIndex[_tokenId] = _to;
        if (_from != address(0)) {
            tokenOwnershipCount[_from]--;
        }
       emit Transfer(_from, _to, _tokenId);
    }
    function transfer10( address _to, uint256 _tokenId1, uint256 _tokenId2, uint256 _tokenId3, uint256 _tokenId4, uint256 _tokenId5, uint256 _tokenId6, uint256 _tokenId7, uint256 _tokenId8, uint256 _tokenId9, uint256 _tokenId10  ) external onlyC {
       require(_to != address(0));
        require(_to != address(this));
     require( SaddleOwnerIndex[_tokenId1] == msg.sender );
     require( SaddleOwnerIndex[_tokenId2] == msg.sender );
     require( SaddleOwnerIndex[_tokenId3] == msg.sender );
     require( SaddleOwnerIndex[_tokenId4] == msg.sender );
     require( SaddleOwnerIndex[_tokenId5] == msg.sender );
     require( SaddleOwnerIndex[_tokenId6] == msg.sender );
     require( SaddleOwnerIndex[_tokenId7] == msg.sender );
     require( SaddleOwnerIndex[_tokenId8] == msg.sender );
     require( SaddleOwnerIndex[_tokenId9] == msg.sender );
     require( SaddleOwnerIndex[_tokenId10] == msg.sender );
      _transfer(msg.sender,  _to,  _tokenId1);
      _transfer(msg.sender,  _to,  _tokenId2);
      _transfer(msg.sender,  _to,  _tokenId3);
      _transfer(msg.sender,  _to,  _tokenId4);
      _transfer(msg.sender,  _to,  _tokenId5);
      _transfer(msg.sender,  _to,  _tokenId6);
      _transfer(msg.sender,  _to,  _tokenId7);
      _transfer(msg.sender,  _to,  _tokenId8);
      _transfer(msg.sender,  _to,  _tokenId9);
      _transfer(msg.sender,  _to,  _tokenId10);
    }
    function _sell(address _from,  uint256 _tokenId, uint256 value) internal {
           uint256 price;
         if(DutchAListed[_tokenId]==true){
        price  = getCurrentSaddlePrice(_tokenId);
         }else{
        price  = saddleIndexPrice[_tokenId];
         }
         if(price==0){
             SaddleIndexForSale[_tokenId]=false;
         }
     if(SaddleIndexForSale[_tokenId]==true){
            require(price<=value);
         uint256 Fee = price / saleFee /2;
          uint256  oPrice= price - Fee - Fee;
            address _to = msg.sender;
            tokenOwnershipCount[_to]++;
            SaddleOwnerIndex[_tokenId] = _to;
            SaddleIndexForSale[_tokenId]=false;
         DutchAListed[_tokenId]=false;
            if (_from != address(0)) {
                tokenOwnershipCount[_from]--;
            }
           emit Transfer(_from, _to, _tokenId);
            uint256 saddleQ = saddleQuality[_tokenId]/10;
             address SaddleSOwner;
              if(saddleQ>=0&&saddleQ<=2){
              SaddleSOwner= SaddleShopO[5];
             }else  if(saddleQ>=2&&saddleQ<=4){
              SaddleSOwner= SaddleShopO[4];
             } else  if(saddleQ>=4&&saddleQ<=6){
             SaddleSOwner=  SaddleShopO[3];
             } else  if(saddleQ>=6&&saddleQ<=8){
             SaddleSOwner=  SaddleShopO[2];
             }else  if(saddleQ>=8&&saddleQ<=10){
             SaddleSOwner=  SaddleShopO[1];
             }else{
             SaddleSOwner= ceoAddress;
             }
             _from.transfer(oPrice);
            uint256 bidExcess = value - oPrice - Fee - Fee;
            _to.transfer(bidExcess);
             ceoAddress.transfer(Fee);
             if(SaddleSOwner!=0){
             SaddleSOwner.transfer(Fee);
             }else {
             ceoAddress.transfer(Fee);
             }
     }else{
          _to.transfer(value);
     }
    }
      function getCurrentSaddlePrice(uint256 _id) public view returns (uint256)  {
      uint256     currentPrice= startDutchAPrice[_id] - DutchADecreaseRate[_id]*(block.number - startDutchABlock[_id]);
  if(currentPrice <=0 ){
      return 0;
  }else if(currentPrice>startDutchAPrice[_id]){
      return 0;
  }else{
    return currentPrice;
  }
  }
      function newDutchPriceRate(uint DecreRate,uint256 _id) external  {
               require(msg.sender==SaddleOwnerIndex[_id]);
               require(DutchAListed[_id]==true);
                DutchADecreaseRate[_id]=DecreRate;
  }
    function setForDutchSale(uint256 _id, uint256 price, uint256 _decreRate) external {
               require(msg.sender==SaddleOwnerIndex[_id]);
                 require(raceListed[_id]==false);
        SaddleShopPrice[_id]=price;
                DutchAListed[_id]=true;
                  startDutchABlock[_id] = block.number;
                  startDutchAPrice[_id] = price;
                 DutchADecreaseRate[_id]= _decreRate;
                SaddleIndexForSale[_id]=true;
    }
    function _newSaddle(
        uint256 _genes1,
        uint256 _genes2,
        uint256 _genes3,
        bool _genes4,
        address _owner
    )
        internal
        returns (uint)
    {
        SaddleAttr memory _saddle = SaddleAttr({
          dna1:_genes1,  
        dna2: _genes2,
        dna3 : _genes3,
        dna4: _genes4
        });
       uint256 newSaddleId;
     newSaddleId = Saddles.push(_saddle)-1;
        require(newSaddleId == uint256(uint32(newSaddleId)));
       saddleQuality[newSaddleId]= (_genes1 +_genes2 + _genes3)/3;
        raceListed[newSaddleId]=false;
       emit Birth(_owner, newSaddleId);
        _transfer(0, _owner, newSaddleId);
        return newSaddleId;  
    }
}
contract SaddleOwnership is SaddleBasis{
  string public constant  name = "CryptoSaddle";
    string public constant symbol = "CSD";
     uint8 public constant decimals = 0; 
    function SaddleForSale(uint256 _tokenId, uint256 price) external { 
     address  ownerof =  SaddleOwnerIndex[_tokenId];
        require(ownerof == msg.sender);
                 require(raceListed[_tokenId]==false);
       uint256 forDutch =  getCurrentSaddlePrice(_tokenId);
      require(forDutch==0||DutchAListed[_tokenId]==false);
        saddleIndexPrice[_tokenId] = price;
       SaddleIndexForSale[_tokenId]= true;
       DutchAListed[_tokenId]=false;
		}
 function changePrice(uint256 _tokenId, uint256 price) external {
     address  ownerof =  SaddleOwnerIndex[_tokenId];
        require(ownerof == msg.sender);
        require(SaddleIndexForSale[_tokenId] == true);
      require(DutchAListed[_tokenId]==false);
             saddleIndexPrice[_tokenId] = price;
		}
 function SaddleNotForSale(uint256 _tokenId) external {
         address  ownerof =  SaddleOwnerIndex[_tokenId];
            require(ownerof == msg.sender);
       SaddleIndexForSale[_tokenId]= false;
         DutchAListed[_tokenId]=false;
    }
    function _owns(address _applicant, uint256 _tokenId) internal view returns (bool) {
        return SaddleOwnerIndex[_tokenId] == _applicant;
    }
    function balanceOf(address _owner) public view returns (uint256 count) {
        return tokenOwnershipCount[_owner];
    }
    function transfer(
        address _to,
        uint256 _tokenId
    )
        external
        payable
    {
        require(_to != address(0));
        require(_to != address(this));
        require(_owns(msg.sender, _tokenId));
       _transfer(msg.sender, _to, _tokenId);
    }
    function approve(
        address _to,
        uint256 _tokenId
    )
        external 
    {
       require(_owns(msg.sender, _tokenId));
        emit Approval(msg.sender, _to, _tokenId);
    }
    function transferFrom(address _from, address _to, uint256 _tokenId ) external payable {
        if(_from != msg.sender){
              require(_to == msg.sender);
                 require(raceListed[_tokenId]==false);
                require(_from==SaddleOwnerIndex[_tokenId]);
               _sell(_from,  _tokenId, msg.value);
        }else{
          _to.transfer(msg.value);
        }
    }
    function totalSupply() public view returns (uint) {
        return Saddles.length;
    }
    function ownerOf(uint256 _tokenId)  external view returns (address owner)  {
        owner = SaddleOwnerIndex[_tokenId];
       return;
    }
    function ownerOfID(uint256 _tokenId)  external view returns (address owner, uint256 tokenId)  {
        owner = SaddleOwnerIndex[_tokenId];
tokenId=_tokenId;
       return;
    }
       function SaddleFS(uint256 _tokenId) external view  returns (bool buyable, uint256 tokenId) {
	bool	forDutchSale=DutchAListed[_tokenId];
	uint256 price;
		if(	forDutchSale==true){
		    	price = getCurrentSaddlePrice(_tokenId);
		}else{
		    	price = saddleIndexPrice[_tokenId];
		}	
		if(price==0){
		    buyable=false;
		}else{
        buyable = SaddleIndexForSale[_tokenId];
		}
        tokenId=_tokenId;
       return;
    }
	function SaddlePr(uint256 _tokenId) external view  returns (uint256 price, uint256 tokenId) {
        price = saddleIndexPrice[_tokenId];
        tokenId=_tokenId;
       return;
    }
 function setSaleFee(uint256 val) external onCTO {
        saleFee = val;
    }
function raceOut(uint256 _tokenIdA) external {
    require(msg.sender==raceDistCon);
      SaddleAttr storage saddleA = Saddles[_tokenIdA];
    saddleA.dna4=true;
	  raceListed[_tokenIdA]=false;
}
function raceRegistration(uint256 _tokenIdA, address owner) external {
   require(msg.sender==raceDistCon);
  require(SaddleOwnerIndex[_tokenIdA]==owner);
      SaddleAttr storage saddleA = Saddles[_tokenIdA];
    require(saddleA.dna4==true);
    require( raceListed[_tokenIdA]==false);
	bool forDutchSale=DutchAListed[_tokenIdA];
	uint256 price;
		if(	forDutchSale==true){
		    	price = getCurrentSaddlePrice(_tokenIdA);
		}else{
		    	price = saddleIndexPrice[_tokenIdA];
		}
    bool buyable;
    if(price==0){
		    buyable=false;
		}else{
        buyable = SaddleIndexForSale[_tokenIdA];
		}
	require(buyable==false);
    saddleA.dna4=false;
    raceListed[_tokenIdA]=true;
}
}
contract SaddleMinting is SaddleOwnership {
    uint256 public  Saddle_Limit = 20000;
        function createSaddle1(   uint256 _genes1, uint256 _genes2,uint256 _genes3, address _owner) external onlyC {
        address SaddleOwner = _owner;
   require(Saddles.length+1 < Saddle_Limit);
              _newSaddle(_genes1, _genes2, _genes3,true, SaddleOwner);
    }
    function createSaddle6(
    uint256 _genes1, 
    uint256 _genes2,
    uint256 _genes3,
    uint256 _genes1a, 
    uint256 _genes2a,
    uint256 _genes3a,
    uint256 _genes1b, 
    uint256 _genes2b,
    uint256 _genes3b,
    address _owner
    ) external onlyC {
        address SaddleOwner = _owner;
   require(Saddles.length+6 < Saddle_Limit);
              _newSaddle(_genes1, _genes2, _genes3,true, SaddleOwner);
              _newSaddle(_genes1a, _genes2a, _genes3a,true, SaddleOwner); 
              _newSaddle(_genes1b, _genes2b, _genes3b,true, SaddleOwner);
              _newSaddle(_genes1, _genes2, _genes3,true, SaddleOwner);
              _newSaddle(_genes1a, _genes2a, _genes3a,true, SaddleOwner); 
              _newSaddle(_genes1b, _genes2b, _genes3b,true, SaddleOwner);
    }
       function _generateNewSaddle(uint256 saddleM_quality ,uint256 maschine_quality, uint256 leader_qual, address _owner) external {
   require(msg.sender==addr_Saddlery);
              _newSaddle(leader_qual, saddleM_quality, maschine_quality,true, _owner);
    }
}
contract GetTheSaddle is SaddleMinting {
    function getSaddle(uint256 _id)
        external
        view
        returns (
        uint256 price,
        uint256 id,
        bool forSale,
        bool forDutchSale,
        uint256 _genes1,
        uint256 _genes2,
        uint256 _genes3,
        bool _genes4
    ) {
        id = uint256(_id);
		forDutchSale=DutchAListed[_id];
		if(	forDutchSale==true){
		    	price = getCurrentSaddlePrice(_id);
		}else{
		    	price = saddleIndexPrice[_id];
		}	
    if(price==0){
		    forSale=false;
		forDutchSale=false;
		}else{
        forSale = SaddleIndexForSale[_id];
		}
        SaddleAttr storage saddle = Saddles[_id];
        _genes1 = saddle.dna1;
        _genes2 = saddle.dna2;
        _genes3 = saddle.dna3;
        _genes4 = saddle.dna4;
    }
}
```

## RQ1_1799f2b23115

SHA-256 `2b71fc96c6308a13f46b3356c117ed670dfe2078bd481405273f0e6b0471bd8c`

```solidity
pragma solidity ^0.4.25;
contract Conquest {
	event onHiveCreated (
        address indexed player,
		uint256 number,
		uint256 time
    );
	event onDroneCreated (
        address indexed player,
		uint256 number,
		uint256 time
    );
	event onEnemyDestroyed (
		address indexed player,
		uint256 time
	);
	modifier onlyAdministrator() {
        address _customerAddress = msg.sender;
        require(administrator_ == _customerAddress);
        _;
    }
    uint256 internal ACTIVATION_TIME = 1544988600;  
	bool internal contractActivated_ = true;
	bool internal payedOut_ = false;
    uint256 internal hiveCost_ = 0.075 ether;
    uint256 internal droneCost_ = 0.01 ether;
	uint256 internal hiveXCommanderFee_ = 50;	
	uint256 internal droneXCommanderFee_ = 15;	
    uint256 internal droneXHiveFee_ = 415;		
    uint8 internal amountHives_ = 8;
    uint8 internal dronesPerDay_ = 20;			
	bool internal conquesting_ = true;
	bool internal conquested_ = false;
    address internal administrator_;
    address internal fundTHCAddress_;
	address internal fundP3DAddress_;
    uint256 internal pot_;
    mapping (address => Pilot) internal pilots_;
    address internal commander_;
    address[] internal hives_;
    address[] internal drones_;
    uint256 internal dronePopulation_;
    constructor() 
        public 
    {
        commander_ = address(this);
        administrator_ = 0x28436C7453EbA01c6EcbC8a9cAa975f0ADE6Fff1;
        fundTHCAddress_ = 0x9674D14AF3EE5dDcD59D3bdcA7435E11bA0ced18;
		fundP3DAddress_ = 0xC0c001140319C5f114F8467295b1F22F86929Ad0;
    }
	function startNewRound() 
		public 
	{
		require(!conquesting_);
		if (!payedOut_) {
			_payout();
		}
		_resetGame();
	}
	function withdrawVault() 
		public 
	{
		address _player = msg.sender;
		uint256 _balance = pilots_[_player].vault;
		require(_balance > 0);
		pilots_[_player].vault = 0;
		_player.transfer(_balance);
	}
	function createCarrierFromVault()
		public 
	{
		address _player = msg.sender;
		uint256 _vault = pilots_[_player].vault;
		require(_vault >= hiveCost_);
		pilots_[_player].vault = _vault - hiveCost_;
		_createHiveInternal(_player);
	}
	function createDroneFromVault()
		public 
	{
		address _player = msg.sender;
		uint256 _vault = pilots_[_player].vault;
		require(_vault >= droneCost_);
		pilots_[_player].vault = _vault - droneCost_;
		_createDroneInternal(_player);
	}    
    function createCarrier() 
		public 
		payable
	{
        address _player = msg.sender;
		require(msg.value == hiveCost_);			
        _createHiveInternal(_player);
    }	
    function createDrone()
        public 
		payable
    {
		address _player = msg.sender;
		require(msg.value == droneCost_);			
        _createDroneInternal(_player);
    }
    function openAt()
        public
        view
        returns(uint256)
    {
        return ACTIVATION_TIME;
    }
    function getHives()
	    public
	    view
	    returns(address[])
	{
	    return hives_;
	}
	function getDrones()
	    public
	    view
	    returns(address[])
	{
	    return drones_;
	}
    function commander()
        public
        view
        returns(address)
    {
        return commander_;
    }
    function conquesting() 
        public
        view
        returns(bool)
    {
        return conquesting_;
    }
	function getCommanderPot()
        public
        view
        returns(uint256)
    {
        uint256 _hivesIncome = hives_.length * hiveCost_;		
        uint256 _dronesIncome = drones_.length * droneCost_;	
        uint256 _pot = pot_ + _hivesIncome + _dronesIncome; 	
		uint256 _fee = _pot / 10;       						
        _pot = _pot - _fee;										
		_hivesIncome = (_hivesIncome * 9) / 10;
        _dronesIncome = (_dronesIncome * 9) / 10;
        uint256 _toCommander = (_hivesIncome * hiveXCommanderFee_) / 100 +		
                               (_dronesIncome * droneXCommanderFee_) / 100;  	
		return _toCommander;
	}
	function getHivePot()
        public
        view
        returns(uint256)
    {
        uint256 _hivesIncome = hives_.length * hiveCost_;		
        uint256 _dronesIncome = drones_.length * droneCost_;	
        uint256 _pot = pot_ + _hivesIncome + _dronesIncome; 	
		uint256 _fee = _pot / 10;       						
        _pot = _pot - _fee;										
		_hivesIncome = (_hivesIncome * 9) / 10;
        _dronesIncome = (_dronesIncome * 9) / 10;
        uint256 _toHives = (_dronesIncome * droneXHiveFee_) / 1000;    			
		return _toHives;
    }
	function getDronePot()
        public
        view
        returns(uint256)
    {
        uint256 _hivesIncome = hives_.length * hiveCost_;		
        uint256 _dronesIncome = drones_.length * droneCost_;	
        uint256 _pot = pot_ + _hivesIncome + _dronesIncome; 	
		uint256 _fee = _pot / 10;       						
        _pot = _pot - _fee;										
		_hivesIncome = (_hivesIncome * 9) / 10;
        _dronesIncome = (_dronesIncome * 9) / 10;
        uint256 _toCommander = (_hivesIncome * hiveXCommanderFee_) / 100 +		
                               (_dronesIncome * droneXCommanderFee_) / 100;  	
        uint256 _toHives = (_dronesIncome * droneXHiveFee_) / 1000;    			
		uint256 _toDrones = _pot - _toHives - _toCommander; 					
		return _toDrones;
    }
	function vaultOf(address _player)
		public
		view
		returns(uint256)
	{
		return pilots_[_player].vault;
	}
	function lastFlight(address _player)
		public
		view
		returns(uint256)
	{
		return pilots_[_player].lastFlight;
	}
    function setGameStatus(bool _active) 
        onlyAdministrator()
        public
    {
        contractActivated_ = _active;
    }
	function _createDroneInternal(address _player)
		internal 
	{
	    require(hives_.length == amountHives_);    					
		require(conquesting_);										
		require(now > pilots_[_player].lastFlight + 60 seconds);	
        drones_.push(_player);
		pilots_[_player].lastFlight = now;
		emit onDroneCreated(_player, drones_.length, now);
		_figthEnemy(_player);
	}
	function _createHiveInternal(address _player) 
		internal 
	{
	    require(now >= ACTIVATION_TIME);                                
	    require(hives_.length < amountHives_);                          
        require(!ownsHive(_player), "Player already owns a hive");      
        hives_.push(_player);
		emit onHiveCreated(_player, hives_.length, now);
	}
    function _figthEnemy(address _player)
        internal
    {
        uint256 _drones = drones_.length;
        uint256 _drone = uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty, _player, _drones))) % 289;
		if (_drone == 42) {
			conquesting_ = false;
			conquested_ = true;
			emit onEnemyDestroyed(_player, now);
		}
    }
    function _payout()
        internal
    {
        uint256 _hivesIncome = amountHives_ * hiveCost_;
        uint256 _dronesIncome = drones_.length * droneCost_;
        uint256 _pot = pot_ + _hivesIncome + _dronesIncome; 	
		uint256 _fee = _pot / 10;       						
        _pot = _pot - _fee;										
		_hivesIncome = (_hivesIncome * 9) / 10;
        _dronesIncome = (_dronesIncome * 9) / 10;
        uint256 _toCommander = (_hivesIncome * hiveXCommanderFee_) / 100 +		
                               (_dronesIncome * droneXCommanderFee_) / 100;  	
        uint256 _toHives = (_dronesIncome * droneXHiveFee_) / 1000;    			
        uint256 _toHive = _toHives / 8;											
        uint256 _toDrones = _pot - _toHives - _toCommander; 					
        if (conquested_) {
            for (uint8 i = 0; i < 8; i++) {
                address _ownerHive = hives_[i];
                pilots_[_ownerHive].vault = pilots_[_ownerHive].vault + _toHive;
                _pot = _pot - _toHive;
            }
            uint256 _squadSize;
            if (drones_.length >= 4) { _squadSize = 4; }				
    		else                     { _squadSize = drones_.length; }	
            for (uint256 j = (drones_.length - _squadSize); j < drones_.length; j++) {
                address _ownerDrone = drones_[j];
                pilots_[_ownerDrone].vault = pilots_[_ownerDrone].vault + (_toDrones / _squadSize);
                _pot = _pot - (_toDrones / _squadSize);
            }
        }
        if (commander_ != address(this)) {
            pilots_[commander_].vault = pilots_[commander_].vault + _toCommander;
            _pot = _pot - _toCommander;
        }
        fundTHCAddress_.transfer(_fee / 2);		
		fundP3DAddress_.transfer(_fee / 2);		
		pot_ = _pot;
		payedOut_ = true;
    }
	function _resetGame() 
		internal 
	{
		if (contractActivated_) {
			address _winner = drones_[drones_.length - 1];
			commander_ = _winner;
			hives_.length = 0;
			drones_.length = 0;
			dronePopulation_ = 0;
			conquesting_ = true;
			conquested_ = false;
			payedOut_ = false;
			ACTIVATION_TIME = now + 5 minutes;
		}
	}
    function ownsHive(address _player) 
        internal
        view
        returns(bool)
    {
        for (uint8 i = 0; i < hives_.length; i++) {
            if (hives_[i] == _player) {
                return true;
            }
        }
        return false;
    }
	struct Pilot {
		uint256 vault;
		uint256 lastFlight;
    }
}
```

## RQ1_3d23e9eaff40

SHA-256 `6e7f57307543d25948b8db85fcf4f17ada605384fff57f8230d48dbd90163628`

```solidity
pragma solidity ^0.4.24;
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
  function isOwner() public {
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
contract EtherCup is Ownable {
  using SafeMath for uint256;
  event NewPlayer(uint tokenId, string name);
  event TokenSold(uint256 tokenId, uint256 oldPrice, address prevOwner, address winner, string name);
  event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);
  uint256 private price = 0.01 ether;
  uint256 private priceLimitOne = 0.05 ether;
  uint256 private priceLimitTwo = 0.5 ether;
  uint256 private priceLimitThree = 2 ether;
  uint256 private priceLimitFour = 5 ether;
  mapping (uint => address) public playerToOwner;
  mapping (address => uint) ownerPlayerCount;
  mapping (uint256 => uint256) public playerToPrice;
  mapping (uint => address) playerApprovals;
  address public ceoAddress;
  struct Player {
    string name;
  }
  Player[] public players;
  modifier onlyCEO() {
    require(msg.sender == ceoAddress);
    _;
  }
  modifier onlyOwnerOf(uint _tokenId) {
    require(msg.sender == playerToOwner[_tokenId]);
    _;
  }
  constructor() public {
    ceoAddress = msg.sender;
  }
  function setCEO(address _newCEO) public onlyCEO {
    require(_newCEO != address(0));
    ceoAddress = _newCEO;
  }
  function createNewPlayer(string _name) public onlyCEO {
    _createPlayer(_name, price);
  }
  function _createPlayer(string _name, uint256 _price) internal {
    uint id = players.push(Player(_name)) - 1;
    playerToOwner[id] = msg.sender;
    ownerPlayerCount[msg.sender] = ownerPlayerCount[msg.sender].add(1);
    emit NewPlayer(id, _name);
    playerToPrice[id] = _price;
  }
  function calculateNextPrice (uint256 _price) public view returns (uint256 _nextPrice) {
    if (_price < priceLimitOne) {
      return _price.mul(200).div(95); 
    } else if (_price < priceLimitTwo) {
      return _price.mul(175).div(95); 
    } else if (_price < priceLimitThree) {
      return _price.mul(150).div(95); 
    } else if (_price < priceLimitFour) {
      return _price.mul(125).div(95); 
    } else {
      return _price.mul(115).div(95); 
    }
  }
  function calculateDevCut (uint256 _price) public pure returns (uint256 _devCut) {
    return _price.mul(5).div(100);
  }
  function purchase(uint256 _tokenId) public payable {
    address oldOwner = playerToOwner[_tokenId];
    address newOwner = msg.sender;
    uint256 sellingPrice = playerToPrice[_tokenId];
    uint256 purchaseExcess = msg.value.sub(sellingPrice);
    require(oldOwner != newOwner);
    require(msg.value >= sellingPrice);
    _transfer(oldOwner, newOwner, _tokenId);
    playerToPrice[_tokenId] = nextPriceOf(_tokenId);
    uint256 devCut = calculateDevCut(sellingPrice);
    uint256 payment = sellingPrice.sub(devCut);
    if (oldOwner != address(this)) {
      oldOwner.transfer(payment);
    }
    if (purchaseExcess > 0){
        newOwner.transfer(purchaseExcess);
    }
    emit TokenSold(_tokenId, sellingPrice, oldOwner, newOwner, players[_tokenId].name);
  }
  function withdrawAll () onlyCEO() public {
    ceoAddress.transfer(address(this).balance);
  }
  function withdrawAmount (uint256 _amount) onlyCEO() public {
    ceoAddress.transfer(_amount);
  }
  function showDevCut () onlyCEO() public view returns (uint256) {
    return address(this).balance;
  }
  function priceOf(uint256 _tokenId) public view returns (uint256 _price) {
    return playerToPrice[_tokenId];
  }
  function priceOfMultiple(uint256[] _tokenIds) public view returns (uint256[]) {
    uint[] memory values = new uint[](_tokenIds.length);
    for (uint256 i = 0; i < _tokenIds.length; i++) {
      values[i] = priceOf(_tokenIds[i]);
    }
    return values;
  }
  function nextPriceOf(uint256 _tokenId) public view returns (uint256 _nextPrice) {
    return calculateNextPrice(priceOf(_tokenId));
  }
  function totalSupply() public view returns (uint256 total) {
    return players.length;
  }
  function balanceOf(address _owner) public view returns (uint256 _balance) {
    return ownerPlayerCount[_owner];
  }
  function ownerOf(uint256 _tokenId) public view returns (address _owner) {
    return playerToOwner[_tokenId];
  }
  function approve(address _to, uint256 _tokenId) public onlyOwnerOf(_tokenId) {
    playerApprovals[_tokenId] = _to;
    emit Approval(msg.sender, _to, _tokenId);
  }
  function transfer(address _to, uint256 _tokenId) public onlyOwnerOf(_tokenId) {
    _transfer(msg.sender, _to, _tokenId);
  }
  function _transfer(address _from, address _to, uint256 _tokenId) private {
    ownerPlayerCount[_to] = ownerPlayerCount[_to].add(1);
    ownerPlayerCount[_from] = ownerPlayerCount[_from].sub(1);
    playerToOwner[_tokenId] = _to;
    emit Transfer(_from, _to, _tokenId);
  }
  function tokensOfOwner(address _owner) public view returns(uint256[] ownerTokens) {
    uint256 tokenCount = balanceOf(_owner);
    if (tokenCount == 0) {
      return new uint256[](0);
    } else {
      uint256[] memory result = new uint256[](tokenCount);
      uint256 totalPlayers = totalSupply();
      uint256 resultIndex = 0;
      uint256 playerId;
      for (playerId = 0; playerId <= totalPlayers; playerId++) {
        if (playerToOwner[playerId] == _owner) {
          result[resultIndex] = playerId;
          resultIndex++;
        }
      }
      return result;
    }
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
```

## RQ1_58c19182bf25

SHA-256 `fcf109825cae8b2b17ba08d0a04ee5d7768673e23df693c27a67c11181951448`

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
  function transferOwnership(address newOwner) public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
  function getOwner() view public returns (address){
    return owner;
  }
}
contract BitLoanex is Ownable {
  using SafeMath for uint256;
  string public constant name = "Bitloanex";
  string public constant symbol = "BTLX";
  uint8 public constant decimals = 8;
  uint256 public rate;
  uint256 public constant CAP = 126000;
  uint256 public constant START = 1514160000;
  uint256 public DAYS = 30;
  uint256 public days_interval = 3;
  uint[9] public deadlines = [START, START.add(1* days_interval * 1 days), START.add(2* days_interval * 1 days), START.add(3* days_interval * 1 days), START.add(4* days_interval * 1 days), START.add(5* days_interval * 1 days), START.add(6* days_interval * 1 days), START.add(7* days_interval * 1 days), START.add(8* days_interval * 1 days)  ];
  uint[9] public rates = [2000, 1800, 1650, 1550, 1450, 1350, 1250, 1150, 1100];
  bool public initialized = true;
  uint256 public raisedAmount = 0;
  uint256 public constant INITIAL_SUPPLY = 10000000000000000;
  uint256 public totalSupply;
  address[] public investors;
  uint[] public timeBought;
  mapping(address => uint256) balances;
  mapping (address => mapping (address => uint256)) internal allowed;
  event Approval(address indexed owner, address indexed spender, uint256 value);
  event Transfer(address indexed from, address indexed to, uint256 value);
  event BoughtTokens(address indexed to, uint256 value);
  function BitLoanex() public {
    totalSupply = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
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
  modifier whenSaleActive() {
  assert(isActive());
  _;
  }
  function initialize(bool _val) public onlyOwner {
    initialized = _val;
  }
  function isActive() public constant returns (bool) {
    return(
      initialized == true &&
      now >= START &&
      now <= START.add(DAYS * 1 days) &&
      goalReached() == false
    );
  }
  function goalReached() private constant returns (bool) {
    return (raisedAmount >= CAP * 1 ether);
  }
  function () public payable {
    buyTokens();
  }
  function buyTokens() public payable {
    require(initialized && now <= START.add(DAYS * 1 days));
    uint256 weiAmount = msg.value;
    uint256 tokens = weiAmount.mul(getRate());
    tokens = tokens.div(1 ether);
    BoughtTokens(msg.sender, tokens);
    balances[msg.sender] = balances[msg.sender].add(tokens);
    balances[owner] = balances[owner].sub(tokens);
    totalSupply.sub(tokens);
    timeBought.push(now) -1;
    raisedAmount = raisedAmount.add(msg.value);
    investors.push(msg.sender) -1;
  }
  function tokenBoughtPerTime(uint _time) public view returns (uint256) {
    uint256 num = 0;
    for(var i = 0; i < timeBought.length; i++){
          if(_time<=timeBought[i]){
              num++;
          }
    }
    return num;
  }
  function getInvestors() view public returns (address[])
  {
      return investors;
  }
  function tokenAvailable() public constant returns (uint256){
     return totalSupply;
  }
  function setRate(uint256 _rate) public onlyOwner
  {
      rate = _rate;
  }
  function setInterval(uint256 _rate) public onlyOwner
  {
      days_interval = _rate;
  }
  function setDays(uint256 _day) public onlyOwner
  {
      DAYS = _day;
  }
  function getRate() public constant returns (uint256){
      if(rate > 0) return rate;
      for(var i = 0; i < deadlines.length; i++)
          if(now<deadlines[i])
              return rates[i-1];
      return rates[rates.length-1];
  }
  function destroy() public onlyOwner {
    selfdestruct(owner);
  }
}

```

## RQ1_80810708faca

SHA-256 `18c6a146be3a52a7741d8f983e5eeefdfcf36aa1d7b46927089cc260fd1f9ca1`

```solidity
contract BCFSafe {
    address owner;
    uint lockTime;
    function TimeDeposit() {
 owner = msg.sender;
 lockTime = now + 30 minutes;
    }
    function returnMyMoney(uint amount){
        if (msg.sender==owner && now > lockTime) {
            owner.send(amount);
        }
    }
}
```

## RQ1_f09f7b47307f

SHA-256 `689a639f0abb145b3c9b9178fa8742b24954e2717f5ce90933358a58b9a7f33e`

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
contract cmctcybermoviechain is ERC20 {
    using SafeMath for uint256;
    address owner = msg.sender;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;    
    string public constant name = "CyberMovieChain";
    string public constant symbol = "CMCT";
    uint public constant decimals = 8;
    uint256 public totalSupply = 20000000000e8;
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
    function cmctcybermovie () public {
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

## RQ1_7dd1efe175e6

SHA-256 `5da0919d8adee863084e6a2abc4345f349bef2156a66c7ee5c2314df5e924e33`

```solidity
pragma solidity 0.5.6;
contract Ownable {
    address private _owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    constructor () internal {
        _owner = msg.sender;
        emit OwnershipTransferred(address(0), _owner);
    }
    function owner() public view returns (address) {
        return _owner;
    }
    modifier onlyOwner() {
        require(isOwner());
        _;
    }
    function isOwner() public view returns (bool) {
        return msg.sender == _owner;
    }
    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }
    function transferOwnership(address newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }
    function _transferOwnership(address newOwner) internal {
        require(newOwner != address(0));
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}
pragma solidity 0.5.6;
library SafeMath
{
  function mul(
    uint256 _factor1,
    uint256 _factor2
  )
    internal
    pure
    returns (uint256 product)
  {
    if (_factor1 == 0)
    {
      return 0;
    }
    product = _factor1 * _factor2;
    require(product / _factor1 == _factor2);
  }
  function div(
    uint256 _dividend,
    uint256 _divisor
  )
    internal
    pure
    returns (uint256 quotient)
  {
    require(_divisor > 0);
    quotient = _dividend / _divisor;
  }
  function sub(
    uint256 _minuend,
    uint256 _subtrahend
  )
    internal
    pure
    returns (uint256 difference)
  {
    require(_subtrahend <= _minuend);
    difference = _minuend - _subtrahend;
  }
  function add(
    uint256 _addend1,
    uint256 _addend2
  )
    internal
    pure
    returns (uint256 sum)
  {
    sum = _addend1 + _addend2;
    require(sum >= _addend1);
  }
  function mod(
    uint256 _dividend,
    uint256 _divisor
  )
    internal
    pure
    returns (uint256 remainder) 
  {
    require(_divisor != 0);
    remainder = _dividend % _divisor;
  }
}
pragma solidity 0.5.6;
interface ERC721TokenReceiver
{
  function onERC721Received(
    address _operator,
    address _from,
    uint256 _tokenId,
    bytes calldata _data
  )
    external
    returns(bytes4);
	function onERC721Received(
    address _from, 
    uint256 _tokenId, 
    bytes calldata _data
  ) 
  external 
  returns 
  (bytes4);
}
pragma solidity ^0.5.6;
library ERC165Checker {
    bytes4 private constant _INTERFACE_ID_INVALID = 0xffffffff;
    bytes4 private constant _INTERFACE_ID_ERC165 = 0x01ffc9a7;
    function _supportsERC165(address account) internal view returns (bool) {
        return _supportsERC165Interface(account, _INTERFACE_ID_ERC165) &&
            !_supportsERC165Interface(account, _INTERFACE_ID_INVALID);
    }
    function _supportsInterface(address account, bytes4 interfaceId) internal view returns (bool) {
        return _supportsERC165(account) &&
            _supportsERC165Interface(account, interfaceId);
    }
    function _supportsAllInterfaces(address account, bytes4[] memory interfaceIds) internal view returns (bool) {
        if (!_supportsERC165(account)) {
            return false;
        }
        for (uint256 i = 0; i < interfaceIds.length; i++) {
            if (!_supportsERC165Interface(account, interfaceIds[i])) {
                return false;
            }
        }
        return true;
    }
    function _supportsERC165Interface(address account, bytes4 interfaceId) private view returns (bool) {
        (bool success, bool result) = _callERC165SupportsInterface(account, interfaceId);
        return (success && result);
    }
    function _callERC165SupportsInterface(address account, bytes4 interfaceId)
        private
        view
        returns (bool success, bool result)
    {
        bytes memory encodedParams = abi.encodeWithSelector(_INTERFACE_ID_ERC165, interfaceId);
        assembly {
            let encodedParams_data := add(0x20, encodedParams)
            let encodedParams_size := mload(encodedParams)
            let output := mload(0x40)    
            mstore(output, 0x0)
            success := staticcall(
                30000,                   
                account,                 
                encodedParams_data,
                encodedParams_size,
                output,
                0x20                     
            )
            result := mload(output)      
        }
    }
}
pragma solidity 0.5.6;
contract Erc721Interface {
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function isApprovedForAll(address _owner, address _operator) external view returns (bool);
    function ownerOf(uint256 _tokenId) external view returns (address _owner);
}
contract KittyInterface {
    mapping (uint256 => address) public kittyIndexToApproved;
    function transfer(address _to, uint256 _tokenId) external;
    function transferFrom(address _from, address _to, uint256 _tokenId) external;
    function ownerOf(uint256 _tokenId) external view returns (address _owner);
}
contract Exchange is Ownable, ERC721TokenReceiver {
    using SafeMath for uint256;
    using SafeMath for uint;
    using ERC165Checker for address;
    address constant internal  CryptoKittiesAddress = 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d;
    bytes4 internal constant ERC721_RECEIVED_THREE_INPUT = 0xf0b9e5ba;
    bytes4 internal constant ERC721_RECEIVED_FOUR_INPUT = 0x150b7a02;
    mapping (address => mapping (uint256 => address)) internal TokenToOwner;
    mapping (address => mapping (address => uint256[])) internal OwnerToTokens;
    mapping (address => mapping(uint256 => uint256)) internal TokenToIndex;
    mapping (address => bytes32[]) internal OwnerToOrders;
    mapping (bytes32 => address) internal OrderToOwner;
    mapping (bytes32 => uint) internal OrderToIndex;
    mapping (bytes32 => address) internal MatchOrderToOwner;
    mapping (bytes32 => bytes32[]) internal OrderToMatchOrders;
    mapping (bytes32 => mapping(bytes32 => uint)) internal OrderToMatchOrderIndex;
    mapping (bytes32 => bool) internal OrderToExist;
    bytes4[] internal SupportNFTInterface;
    struct OrderObj {
        address owner;
        address contractAddress;
        uint256 tokenId;
    }
    mapping (bytes32 => OrderObj) internal HashToOrderObj;
    event ReceiveToken(
        address indexed _from, 
        address _contractAddress, 
        uint256 _tokenId
    );
    event SendBackToken(
        address indexed _owner, 
        address _contractAddress, 
        uint256 _tokenId
    );
    event SendToken(
        address indexed _to, 
        address _contractAddress, 
        uint256 _tokenId
    );
    event CreateOrderObj(
        bytes32 indexed _hash,
        address _owner,
        address _contractAddress,
        uint256 _tokenId   
    );
    event CreateOrder(
        address indexed _from,
        bytes32 indexed _orderHash,
        address _contractAddress,
        uint256 _tokenId
    );
    event CreateMatchOrder(
        address indexed _from,
        bytes32 indexed _orderHash,
        bytes32 indexed _matchOrderHash,
        address _contractAddress,
        uint256 _tokenId
    );
    event DeleteOrder(
        address indexed _from,
        bytes32 indexed _orderHash
    );
    event DeleteMatchOrder(
        address indexed _from,
        bytes32 indexed _orderHash,
        bytes32 indexed _matchOrderHash
    );
    modifier onlySenderIsOriginalOwner(
        address contractAddress, 
        uint256 tokenId
    ) 
    {
        require(TokenToOwner[contractAddress][tokenId] == msg.sender, "original owner should be message sender");
        _;
    }
    constructor () public {
        SupportNFTInterface.push(0x80ac58cd);
        SupportNFTInterface.push(0x780e9d63);
        SupportNFTInterface.push(0x5b5e139f);
    }
    function addSupportNFTInterface(
        bytes4 interface_id
    )
    external
    onlyOwner()
    {
        SupportNFTInterface.push(interface_id);
    }
    function onERC721Received(
        address _from, 
        uint256 _tokenId, 
        bytes calldata _data
    ) 
    external 
    returns (bytes4)
    {
        return ERC721_RECEIVED_THREE_INPUT;
    }
    function onERC721Received(
        address _operator,
        address _from,
        uint256 _tokenId,
        bytes calldata data
    )
    external
    returns(bytes4)
    {
        return ERC721_RECEIVED_FOUR_INPUT;
    }
    function createOrder(
        address contractAddress, 
        uint256 tokenId
    ) 
    external 
    onlySenderIsOriginalOwner(
        contractAddress, 
        tokenId
    ) 
    {
        bytes32 orderHash = keccak256(abi.encodePacked(contractAddress, tokenId, msg.sender));
        require(OrderToOwner[orderHash] != msg.sender, "Order already exist");
        _addOrder(msg.sender, orderHash);
        emit CreateOrder(msg.sender, orderHash, contractAddress, tokenId);
    }
    function _addOrder(
        address sender, 
        bytes32 orderHash
    ) 
    internal 
    {
        uint index = OwnerToOrders[sender].push(orderHash).sub(1);
        OrderToOwner[orderHash] = sender;
        OrderToIndex[orderHash] = index;
        OrderToExist[orderHash] = true;
    }
    function deleteOrder(
        bytes32 orderHash
    )
    external
    {
        require(OrderToOwner[orderHash] == msg.sender, "this order hash not belongs to this address");
        _removeOrder(msg.sender, orderHash);
        emit DeleteOrder(msg.sender, orderHash);
    }
    function _removeOrder(
        address sender,
        bytes32 orderHash
    )
    internal
    {
        OrderToExist[orderHash] = false;
        delete OrderToOwner[orderHash];
        uint256 orderIndex = OrderToIndex[orderHash];
        uint256 lastOrderIndex = OwnerToOrders[sender].length.sub(1);
        if (lastOrderIndex != orderIndex){
            bytes32 lastOwnerOrder = OwnerToOrders[sender][lastOrderIndex];
            OwnerToOrders[sender][orderIndex] = lastOwnerOrder;
            OrderToIndex[lastOwnerOrder] = orderIndex;
        }
        OwnerToOrders[sender].length--;
    }
    function createMatchOrder(
        address contractAddress,
        uint256 tokenId, 
        bytes32 orderHash
    ) 
    external 
    onlySenderIsOriginalOwner(
        contractAddress, 
        tokenId
    ) 
    {
        bytes32 matchOrderHash = keccak256(abi.encodePacked(contractAddress, tokenId, msg.sender));
        require(OrderToOwner[matchOrderHash] != msg.sender, "Order already exist");
        _addMatchOrder(matchOrderHash, orderHash);
        emit CreateMatchOrder(msg.sender, orderHash, matchOrderHash, contractAddress, tokenId);
    }
    function _addMatchOrder(
        bytes32 matchOrderHash, 
        bytes32 orderHash
    ) 
    internal 
    {
        uint inOrderIndex = OrderToMatchOrders[orderHash].push(matchOrderHash).sub(1);
        OrderToMatchOrderIndex[orderHash][matchOrderHash] = inOrderIndex;
    }
    function deleteMatchOrder(
        bytes32 matchOrderHash,
        bytes32 orderHash
    )
    external
    {
        require(MatchOrderToOwner[matchOrderHash] == msg.sender, "match order doens't belong to this address" );
        require(OrderToExist[orderHash] == true, "this order is not exist");
        _removeMatchOrder(orderHash, matchOrderHash);
        emit DeleteMatchOrder(msg.sender, orderHash, matchOrderHash);
    }
    function _removeMatchOrder(
        bytes32 orderHash,
        bytes32 matchOrderHash
    )
    internal
    {
        uint256 matchOrderIndex = OrderToMatchOrderIndex[orderHash][matchOrderHash];
        uint256 lastMatchOrderIndex = OrderToMatchOrders[orderHash].length.sub(1);
        if (lastMatchOrderIndex != matchOrderIndex){
            bytes32 lastMatchOrder = OrderToMatchOrders[orderHash][lastMatchOrderIndex];
            OrderToMatchOrders[orderHash][matchOrderIndex] = lastMatchOrder;
            OrderToMatchOrderIndex[orderHash][lastMatchOrder] = matchOrderIndex;
        }
        OrderToMatchOrders[orderHash].length--;
    }
    function exchangeToken(
        bytes32 order,
        bytes32 matchOrder
    ) 
    external 
    {
        require(OrderToOwner[order] == msg.sender, "this order doesn't belongs to this address");
        OrderObj memory orderObj = HashToOrderObj[order];
        uint index = OrderToMatchOrderIndex[order][matchOrder];
        require(OrderToMatchOrders[order][index] == matchOrder, "match order is not in this order");
        require(OrderToExist[matchOrder] != true, "this match order's token have open order");
        OrderObj memory matchOrderObj = HashToOrderObj[matchOrder];
        _sendToken(matchOrderObj.owner, orderObj.contractAddress, orderObj.tokenId);
        _sendToken(orderObj.owner, matchOrderObj.contractAddress, matchOrderObj.tokenId);
        _removeMatchOrder(order, matchOrder);
        _removeOrder(msg.sender, order);
    }
    function receiveErc721Token(
        address contractAddress, 
        uint256 tokenId
    ) 
    external  
    {
        bool checkSupportErc165Interface = false;
        if(contractAddress != CryptoKittiesAddress){
            for(uint i = 0; i < SupportNFTInterface.length; i++){
                if(contractAddress._supportsInterface(SupportNFTInterface[i]) == true){
                    checkSupportErc165Interface = true;
                }
            }
            require(checkSupportErc165Interface == true, "not supported Erc165 Interface");
            Erc721Interface erc721Contract = Erc721Interface(contractAddress);
            require(erc721Contract.isApprovedForAll(msg.sender,address(this)) == true, "contract doesn't have power to control this token id");
            erc721Contract.transferFrom(msg.sender, address(this), tokenId);
        }else {
            KittyInterface kittyContract = KittyInterface(contractAddress);
            require(kittyContract.kittyIndexToApproved(tokenId) == address(this), "contract doesn't have power to control this cryptoKitties's id");
            kittyContract.transferFrom(msg.sender, address(this), tokenId);
        }
        _addToken(msg.sender, contractAddress, tokenId);
        emit ReceiveToken(msg.sender, contractAddress, tokenId);
    }
    function _addToken(
        address sender, 
        address contractAddress, 
        uint256 tokenId
    ) 
    internal 
    {   
        bytes32 matchOrderHash = keccak256(abi.encodePacked(contractAddress, tokenId, sender));
        MatchOrderToOwner[matchOrderHash] = sender;
        HashToOrderObj[matchOrderHash] = OrderObj(sender,contractAddress,tokenId);
        TokenToOwner[contractAddress][tokenId] = sender;
        uint index = OwnerToTokens[sender][contractAddress].push(tokenId).sub(1);
        TokenToIndex[contractAddress][tokenId] = index;
        emit CreateOrderObj(matchOrderHash, sender, contractAddress, tokenId);
    }
    function sendBackToken(
        address contractAddress, 
        uint256 tokenId
    ) 
    external 
    onlySenderIsOriginalOwner(
        contractAddress, 
        tokenId
    ) 
    {
        bytes32 orderHash = keccak256(abi.encodePacked(contractAddress, tokenId, msg.sender));
        if(OrderToExist[orderHash] == true) {
            _removeOrder(msg.sender, orderHash);
        }
        _sendToken(msg.sender, contractAddress, tokenId);
        emit SendBackToken(msg.sender, contractAddress, tokenId);
    }  
    function _sendToken(
        address sendAddress,
        address contractAddress, 
        uint256 tokenId
    )
    internal
    {   
        if(contractAddress != CryptoKittiesAddress){
            Erc721Interface erc721Contract = Erc721Interface(contractAddress);
            require(erc721Contract.ownerOf(tokenId) == address(this), "exchange contract should have this token");
            erc721Contract.transferFrom(address(this), sendAddress, tokenId);
        }else{
            KittyInterface kittyContract = KittyInterface(contractAddress);
            require(kittyContract.ownerOf(tokenId) == address(this), "exchange contract should have this token");
            kittyContract.transfer(sendAddress, tokenId);
        }
        _removeToken(contractAddress, tokenId);
        emit SendToken(sendAddress, contractAddress, tokenId);
    }
    function _removeToken(
        address contractAddress, 
        uint256 tokenId
    ) 
    internal 
    {
        address owner = TokenToOwner[contractAddress][tokenId];
        bytes32 orderHash = keccak256(abi.encodePacked(contractAddress, tokenId, owner));
        delete HashToOrderObj[orderHash];
        delete MatchOrderToOwner[orderHash];
        delete TokenToOwner[contractAddress][tokenId];
        uint256 tokenIndex = TokenToIndex[contractAddress][tokenId];
        uint256 lastOwnerTokenIndex = OwnerToTokens[owner][contractAddress].length.sub(1);
        if (lastOwnerTokenIndex != tokenIndex){
            uint256 lastOwnerToken = OwnerToTokens[owner][contractAddress][lastOwnerTokenIndex];
            OwnerToTokens[owner][contractAddress][tokenIndex] = lastOwnerToken;
            TokenToIndex[contractAddress][lastOwnerToken] = tokenIndex;
        }
        OwnerToTokens[owner][contractAddress].length--;
    }
    function getTokenOwner(
        address contractAddress, 
        uint256 tokenId
    ) 
    external 
    view 
    returns (address)
    {
        return TokenToOwner[contractAddress][tokenId];
    }
    function getOwnerTokens(
        address ownerAddress, 
        address contractAddress
    ) 
    external 
    view 
    returns (uint256[] memory)
    {
        return OwnerToTokens[ownerAddress][contractAddress];
    }
    function getTokenIndex(
        address contractAddress, 
        uint256 tokenId
    ) 
    external 
    view
    returns (uint256)
    {
        return TokenToIndex[contractAddress][tokenId];
    }
    function getOwnerOrders(
        address ownerAddress
    ) 
    external 
    view 
    returns (bytes32[] memory){
        return OwnerToOrders[ownerAddress];
    }
    function getOrderOwner(
        bytes32 order
    ) 
    external 
    view 
    returns (address)
    {
        return OrderToOwner[order];
    }
    function getOrderIndex(
        bytes32 order
    ) 
    external 
    view 
    returns (uint)
    {
        return OrderToIndex[order];
    }
    function getOrderExist(
        bytes32 order
    )
    external
    view
    returns (bool){
        return OrderToExist[order];
    }
    function getMatchOrderOwner(
        bytes32 matchOrder
    ) 
    external 
    view 
    returns (address)
    {
        return MatchOrderToOwner[matchOrder];
    }
    function getOrderMatchOrderIndex(
        bytes32 order,
        bytes32 matchOrder
    ) 
    external 
    view 
    returns (uint)
    {
        return OrderToMatchOrderIndex[order][matchOrder];
    }
    function getOrderMatchOrders(
        bytes32 order
    ) 
    external 
    view 
    returns (bytes32[] memory)
    {
        return OrderToMatchOrders[order];
    }
    function getHashOrderObj(
        bytes32 hashOrder
    )
    external
    view
    returns(
        address, 
        address, 
        uint256
    )
    {
        OrderObj memory orderObj = HashToOrderObj[hashOrder];
        return(
            orderObj.owner,
            orderObj.contractAddress,
            orderObj.tokenId
        );
    }
}
```

## RQ1_8efe2f574918

SHA-256 `9cd83dceb0893853e29cbb13d63a3912acb1be71dc34ded9c7199444988b991e`

```solidity
pragma solidity 0.4.24;
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
contract database {
    using SafeMath for uint256;
    struct participant {
        address eth_address; 
        uint256 topl_address; 
        uint256 arbits; 
        uint256 num_of_pro_rata_tokens_alloted;
        bool arbits_kyc_whitelist; 
        uint8 num_of_uses;
    }
    mapping(address => bool) public sale_owners;
    mapping(address => bool) public owners;
    mapping(address => bool) public masters;
    mapping(address => bool) public kycers;
    mapping(address => participant) public participants;
    address[] public participant_keys;
    bool public arbits_presale_open = false; 
    bool public iconiq_presale_open = false; 
    bool public arbits_sale_open = false; 
    uint256 public pre_kyc_bonus_denominator;
    uint256 public pre_kyc_bonus_numerator;
    uint256 public pre_kyc_iconiq_bonus_denominator;
    uint256 public pre_kyc_iconiq_bonus_numerator;
    uint256 public contrib_arbits_min;
    uint256 public contrib_arbits_max;
    uint256 public presale_arbits_per_ether;        
    uint256 public presale_iconiq_arbits_per_ether; 
    uint256 public presale_arbits_total = 18000000;
    uint256 public presale_arbits_sold;
    uint256 public sale_arbits_per_ether;
    uint256 public sale_arbits_total;
    uint256 public sale_arbits_sold;
    constructor() public {
        owners[msg.sender] = true;
    }
    function add_owner(address __subject) public only_owner {
        owners[__subject] = true;
    }
    function remove_owner(address __subject) public only_owner {
        owners[__subject] = false;
    }
    function add_master(address _subject) public only_owner {
        masters[_subject] = true;
    }
    function remove_master(address _subject) public only_owner {
        masters[_subject] = false;
    }
    function add_kycer(address _subject) public only_owner {
        kycers[_subject] = true;
    }
    function remove_kycer(address _subject) public only_owner {
        kycers[_subject] = false;
    }
    modifier log_participant_update(address __eth_address) {
        participant_keys.push(__eth_address); 
        _;
    }
    modifier only_owner() {
        require(owners[msg.sender]);
        _;
    }
    modifier only_kycer() {
        require(kycers[msg.sender]);
        _;
    }
    modifier only_master_or_owner() {
        require(masters[msg.sender] || owners[msg.sender]);
        _;
    }
    function get_sale_owner(address _a) public view returns(bool) {
        return sale_owners[_a];
    }
    function get_contrib_arbits_min() public view returns(uint256) {
        return contrib_arbits_min;
    }
    function get_contrib_arbits_max() public view returns(uint256) {
        return contrib_arbits_max;
    }
    function get_pre_kyc_bonus_numerator() public view returns(uint256) {
        return pre_kyc_bonus_numerator;
    }
    function get_pre_kyc_bonus_denominator() public view returns(uint256) {
        return pre_kyc_bonus_denominator;
    }
    function get_pre_kyc_iconiq_bonus_numerator() public view returns(uint256) {
        return pre_kyc_iconiq_bonus_numerator;
    }
    function get_pre_kyc_iconiq_bonus_denominator() public view returns(uint256) {
        return pre_kyc_iconiq_bonus_denominator;
    }
    function get_presale_iconiq_arbits_per_ether() public view returns(uint256) {
        return (presale_iconiq_arbits_per_ether);
    }
    function get_presale_arbits_per_ether() public view returns(uint256) {
        return (presale_arbits_per_ether);
    }
    function get_presale_arbits_total() public view returns(uint256) {
        return (presale_arbits_total);
    }
    function get_presale_arbits_sold() public view returns(uint256) {
        return (presale_arbits_sold);
    }
    function get_sale_arbits_per_ether() public view returns(uint256) {
        return (sale_arbits_per_ether);
    }
    function get_sale_arbits_total() public view returns(uint256) {
        return (sale_arbits_total);
    }
    function get_sale_arbits_sold() public view returns(uint256) {
        return (sale_arbits_sold);
    }
    function set_sale_owner(address _a, bool _v) public only_master_or_owner {
        sale_owners[_a] = _v;
    }
    function set_contrib_arbits_min(uint256 _v) public only_master_or_owner {
        contrib_arbits_min = _v;
    }
    function set_contrib_arbits_max(uint256 _v) public only_master_or_owner {
        contrib_arbits_max = _v;
    }
    function set_pre_kyc_bonus_numerator(uint256 _v) public only_master_or_owner {
        pre_kyc_bonus_numerator = _v;
    }
    function set_pre_kyc_bonus_denominator(uint256 _v) public only_master_or_owner {
        pre_kyc_bonus_denominator = _v;
    }
    function set_pre_kyc_iconiq_bonus_numerator(uint256 _v) public only_master_or_owner {
        pre_kyc_iconiq_bonus_numerator = _v;
    }
    function set_pre_kyc_iconiq_bonus_denominator(uint256 _v) public only_master_or_owner {
        pre_kyc_iconiq_bonus_denominator = _v;
    }
    function set_presale_iconiq_arbits_per_ether(uint256 _v) public only_master_or_owner {
        presale_iconiq_arbits_per_ether = _v;
    }
    function set_presale_arbits_per_ether(uint256 _v) public only_master_or_owner {
        presale_arbits_per_ether = _v;
    }
    function set_presale_arbits_total(uint256 _v) public only_master_or_owner {
        presale_arbits_total = _v;
    }
    function set_presale_arbits_sold(uint256 _v) public only_master_or_owner {
        presale_arbits_sold = _v;
    }
    function set_sale_arbits_per_ether(uint256 _v) public only_master_or_owner {
        sale_arbits_per_ether = _v;
    }
    function set_sale_arbits_total(uint256 _v) public only_master_or_owner {
        sale_arbits_total = _v;
    }
    function set_sale_arbits_sold(uint256 _v) public only_master_or_owner {
        sale_arbits_sold = _v;
    }
    function get_participant(address _a) public view returns(
        address,
        uint256,
        uint256,
        uint256,
        bool,
        uint8
    ) {
        participant storage subject = participants[_a];
        return (
            subject.eth_address,
            subject.topl_address,
            subject.arbits,
            subject.num_of_pro_rata_tokens_alloted,
            subject.arbits_kyc_whitelist,
            subject.num_of_uses
        );
    }
    function get_participant_num_of_uses(address _a) public view returns(uint8) {
        return (participants[_a].num_of_uses);
    }
    function get_participant_topl_address(address _a) public view returns(uint256) {
        return (participants[_a].topl_address);
    }
    function get_participant_arbits(address _a) public view returns(uint256) {
        return (participants[_a].arbits);
    }
    function get_participant_num_of_pro_rata_tokens_alloted(address _a) public view returns(uint256) {
        return (participants[_a].num_of_pro_rata_tokens_alloted);
    }
    function get_participant_arbits_kyc_whitelist(address _a) public view returns(bool) {
        return (participants[_a].arbits_kyc_whitelist);
    }
    function set_participant(
        address _a,
        uint256 _ta,
        uint256 _arbits,
        uint256 _prta,
        bool _v3,
        uint8 _nou
    ) public only_master_or_owner log_participant_update(_a) {
        participant storage subject = participants[_a];
        subject.eth_address = _a;
        subject.topl_address = _ta;
        subject.arbits = _arbits;
        subject.num_of_pro_rata_tokens_alloted = _prta;
        subject.arbits_kyc_whitelist = _v3;
        subject.num_of_uses = _nou;
    }
    function set_participant_num_of_uses(
        address _a,
        uint8 _v
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].num_of_uses = _v;
    }
    function set_participant_topl_address(
        address _a,
        uint256 _ta
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].topl_address = _ta;
    }
    function set_participant_arbits(
        address _a,
        uint256 _v
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].arbits = _v;
    }
    function set_participant_num_of_pro_rata_tokens_alloted(
        address _a,
        uint256 _v
    ) public only_master_or_owner log_participant_update(_a) {
        participants[_a].num_of_pro_rata_tokens_alloted = _v;
    }
    function set_participant_arbits_kyc_whitelist(
        address _a,
        bool _v
    ) public only_kycer log_participant_update(_a) {
        participants[_a].arbits_kyc_whitelist = _v;
    }
    function get_iconiq_presale_open() public view only_master_or_owner returns(bool) {
        return iconiq_presale_open;
    }
    function get_arbits_presale_open() public view only_master_or_owner returns(bool) {
        return arbits_presale_open;
    }
    function get_arbits_sale_open() public view only_master_or_owner returns(bool) {
        return arbits_sale_open;
    }
    function set_iconiq_presale_open(bool _v) public only_master_or_owner {
        iconiq_presale_open = _v;
    }
    function set_arbits_presale_open(bool _v) public only_master_or_owner {
        arbits_presale_open = _v;
    }
    function set_arbits_sale_open(bool _v) public only_master_or_owner {
        arbits_sale_open = _v;
    }
}
library topl_database_lib {
    function get_participant(address db, address _a) internal view returns(
        address,
        uint256,
        uint256,
        uint256,
        bool,
        uint8
    ) {
        return database(db).get_participant(_a);
    }
    function get_topl_address(address db, address _a) internal view returns(uint256) {
        return database(db).get_participant_topl_address(_a);
    }
    function get_arbits(address db, address _a) internal view returns(uint256) {
        return database(db).get_participant_arbits(_a);
    }
    function get_iconiq_tokens(address db, address _a) internal view returns(uint256) {
        return database(db).get_participant_num_of_pro_rata_tokens_alloted(_a);
    }
    function get_arbits_whitelist(address db, address _a) internal view returns(bool) {
        return database(db).get_participant_arbits_kyc_whitelist(_a);
    }
    function get_num_of_uses(address db, address _a) internal view returns(uint8) {
        return database(db).get_participant_num_of_uses(_a);
    }
    function set_participant(
        address db,
        address _a,
        uint256 _ta,
        uint256 _arbits,
        uint256 _prta,
        bool _v3,
        uint8 _nou
    ) internal {
        database(db).set_participant(_a, _ta, _arbits, _prta, _v3, _nou);
        emit e_set_participant(_a, _ta, _arbits, _prta, _v3, _nou);
    }
    function set_topl_address(address db, address _a, uint256 _ta) internal {
        database(db).set_participant_topl_address(_a, _ta);
        emit e_set_topl_address(_a, _ta);
    }
    function set_arbits(address db, address _a, uint256 _v) internal {
        database(db).set_participant_arbits(_a, _v);
        emit e_set_arbits(_a, _v);
    }
    function set_iconiq_tokens(address db, address _a, uint256 _v) internal {
        database(db).set_participant_num_of_pro_rata_tokens_alloted(_a, _v);
        emit e_set_iconiq_tokens(_a, _v);
    }
    function set_arbits_whitelist(address db, address _a, bool _v) internal {
        database(db).set_participant_arbits_kyc_whitelist(_a, _v);
        emit e_set_arbits_whitelist(_a, _v);
    }
    function set_num_of_uses(address db, address _a, uint8 _v) internal {
        database(db).set_participant_num_of_uses(_a, _v);
        emit e_set_num_of_uses(_a, _v);
    }
    function add_arbits(address db, address _a, uint256 _v) internal {
        uint256 c = database(db).get_participant_arbits(_a) + _v;     
        assert(c >= database(db).get_participant_arbits(_a)); 
        database(db).set_participant_arbits(
            _a,
            (database(db).get_participant_arbits(_a) + _v)
        );
        emit e_add_arbits(_a, _v);
    }
    function sub_arbits(address db, address _a, uint256 _v) internal {
        assert(_v <= database(db).get_participant_arbits(_a)); 
        database(db).set_participant_arbits(
            _a,
            (database(db).get_participant_arbits(_a) - _v)
        );
        emit e_sub_arbits(_a, _v);
    }
    function get_pre_kyc_iconiq_bonus_numerator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_iconiq_bonus_numerator();
    }
    function get_pre_kyc_iconiq_bonus_denominator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_iconiq_bonus_denominator();
    }
    function get_iconiq_presale_open(address db) internal view returns(bool) {
        return database(db).get_iconiq_presale_open();
    }
    function get_presale_iconiq_arbits_per_ether(address db) internal view returns(uint256) {
        return database(db).get_presale_iconiq_arbits_per_ether();
    }
    function set_pre_kyc_iconiq_bonus_numerator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_iconiq_bonus_numerator(_v);
        emit e_set_pre_kyc_iconiq_bonus_numerator(_v);
    }
    function set_pre_kyc_iconiq_bonus_denominator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_iconiq_bonus_denominator(_v);
        emit e_set_pre_kyc_iconiq_bonus_denominator(_v);
    }
    function set_iconiq_presale_open(address db, bool _v) internal {
        database(db).set_iconiq_presale_open(_v);
        emit e_set_iconiq_presale_open(_v);
    }
    function set_presale_iconiq_arbits_per_ether(address db, uint256 _v) internal {
        database(db).set_presale_iconiq_arbits_per_ether(_v);
        emit e_set_presale_iconiq_arbits_per_ether(_v);
    }
    function get_pre_kyc_bonus_numerator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_bonus_numerator();
    }
    function get_pre_kyc_bonus_denominator(address db) internal view returns(uint256) {
        return database(db).get_pre_kyc_bonus_denominator();
    }
    function get_arbits_presale_open(address db) internal view returns(bool) {
        return database(db).get_arbits_presale_open();
    }
    function get_presale_arbits_per_ether(address db) internal view returns(uint256) {
        return database(db).get_presale_arbits_per_ether();
    }
    function set_pre_kyc_bonus_numerator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_bonus_numerator(_v);
        emit e_set_pre_kyc_bonus_numerator(_v);
    }
    function set_pre_kyc_bonus_denominator(address db, uint256 _v) internal {
        database(db).set_pre_kyc_bonus_denominator(_v);
        emit e_set_pre_kyc_bonus_denominator(_v);
    }
    function set_arbits_presale_open(address db, bool _v) internal {
        database(db).set_arbits_presale_open(_v);
        emit e_set_arbits_presale_open(_v);
    }
    function set_presale_arbits_per_ether(address db, uint256 _v) internal {
        database(db).set_presale_arbits_per_ether(_v);
        emit e_set_presale_arbits_per_ether(_v);
    }
    function get_presale_arbits_total(address db) internal view returns(uint256) {
        return database(db).get_presale_arbits_total();
    }
    function get_presale_arbits_sold(address db) internal view returns(uint256) {
        return database(db).get_presale_arbits_sold();
    }
    function get_arbits_max_contribution(address db) internal view returns(uint256) {
        return database(db).get_contrib_arbits_max();
    }
    function get_arbits_min_contribution(address db) internal view returns(uint256) {
        return database(db).get_contrib_arbits_min();
    }
    function set_presale_arbits_total(address db, uint256 _v) internal {
        database(db).set_presale_arbits_total(_v);
        emit e_set_presale_arbits_total(_v);
    }
    function set_presale_arbits_sold(address db, uint256 _v) internal {
        database(db).set_presale_arbits_sold(_v);
        emit e_set_presale_arbits_sold(_v);
    }
    function set_arbits_max_contribution(address db, uint256 _v) internal {
        database(db).set_contrib_arbits_max(_v);
        emit e_set_arbits_max_contribution(_v);
    }
    function set_arbits_min_contribution(address db, uint256 _v) internal {
        database(db).set_contrib_arbits_min(_v);
        emit e_set_arbits_min_contribution(_v);
    }
    function add_presale_arbits_sold(address db, uint256 _v) internal {
        uint256 c = database(db).get_presale_arbits_sold() + _v;     
        assert(c >= database(db).get_presale_arbits_sold()); 
        database(db).set_presale_arbits_sold(
            (database(db).get_presale_arbits_sold() + _v)
        );
        emit e_add_presale_arbits_sold(_v);
    }
    function sub_presale_arbits_sold(address db, uint256 _v) internal {
        assert(_v <= database(db).get_presale_arbits_sold()); 
        database(db).set_presale_arbits_sold(
            (database(db).get_presale_arbits_sold() - _v)
        );
        emit e_sub_presale_arbits_sold(_v);
    }
    function set_sale_owner(address db, address _a, bool _v) internal {
        database(db).set_sale_owner(_a, _v);
    }
    function get_sale_owner(address db, address _a) internal view returns(bool) {
        return database(db).get_sale_owner(_a);
    }
    event e_set_sale_owner(address, bool);
    event e_set_num_of_uses(address, uint8);
    event e_set_arbits_whitelist(address, bool);
    event e_set_participant(address, uint256, uint256, uint256, bool, uint8);
    event e_set_topl_address(address, uint256);
    event e_set_arbits(address, uint256);
    event e_set_iconiq_tokens(address, uint256);
    event e_add_arbits(address, uint256);
    event e_sub_arbits(address, uint256);
    event e_set_pre_kyc_bonus_numerator(uint256);
    event e_set_pre_kyc_bonus_denominator(uint256);
    event e_set_iconiq_presale_open(bool);
    event e_set_arbits_presale_open(bool);
    event e_set_presale_iconiq_arbits_per_ether(uint256);
    event e_set_presale_arbits_per_ether(uint256);
    event e_set_presale_arbits_total(uint256);
    event e_set_presale_arbits_sold(uint256);
    event e_add_presale_arbits_sold(uint256);
    event e_sub_presale_arbits_sold(uint256);
    event e_set_arbits_max_contribution(uint256);
    event e_set_arbits_min_contribution(uint256);
    event e_set_pre_kyc_iconiq_bonus_numerator(uint256);
    event e_set_pre_kyc_iconiq_bonus_denominator(uint256);
}
contract iconiq_presale {
    using topl_database_lib for address;
    using SafeMath for uint256;
    address public owner;
    address public db;
    struct participant {
        address eth_address; 
        uint256 topl_address; 
        uint256 arbits; 
        uint256 num_of_pro_rata_tokens_alloted;
        bool arbits_kyc_whitelist; 
        uint8 num_of_uses;
    }
    constructor(address __db) public {
        db = __db;
        owner = msg.sender;
    }
    function owner_linkage() public { 
        db.set_sale_owner(owner, true);
    }
    modifier only_owner() {
        require(db.get_sale_owner(msg.sender));
        _;
    }
    function add_owner(address __subject) public only_owner {
        db.set_sale_owner(__subject, true);
        emit e_add_owner(msg.sender, __subject);
    }
    function remove_owner(address __subject) public only_owner {
        db.set_sale_owner(__subject, false);
        emit e_remove_owner(msg.sender, __subject);
    }
    function participate_in_arbits_presale_crypto() public payable presale_open use_count {
        (                                                                  
            address p1,                                                    
            uint256 p2,                                                    
            uint256 p3,                                                    
            uint256 p4,                                                    
            bool p5,                                                       
            uint8 p6                                                       
        ) = db.get_participant(msg.sender);                                
        participant memory subject = participant(p1, p2, p3, p4, p5, p6);  
        require(subject.num_of_pro_rata_tokens_alloted > 0); 
        uint256 subject_tokens_to_add_at_iconiq_price = msg.value.mul(db.get_presale_iconiq_arbits_per_ether()).div(1 ether);  
        uint256 subject_tokens_to_add_at_reg_price = msg.value.mul(db.get_presale_arbits_per_ether()).div(1 ether);            
        uint256 amount_of_pro_rata_tokens_subject_can_get = subject.num_of_pro_rata_tokens_alloted;                                        
        uint256 subject_tokens_to_add = 0;                                                                                                 
        if (amount_of_pro_rata_tokens_subject_can_get >= subject.arbits.add(subject_tokens_to_add_at_iconiq_price)) {                      
            subject_tokens_to_add = subject_tokens_to_add_at_iconiq_price;  
        } else {                                                                                                                           
            if (subject.arbits < amount_of_pro_rata_tokens_subject_can_get) {                                                              
                uint256 delta = amount_of_pro_rata_tokens_subject_can_get.sub(subject.arbits);  
                subject_tokens_to_add = delta.add(                                              
                    subject_tokens_to_add_at_iconiq_price                                       
                    .sub(delta)                                                                 
                    .mul(db.get_presale_arbits_per_ether())                                     
                    .div(db.get_presale_iconiq_arbits_per_ether())                              
                );                                                                              
            } else {                                                                                                                       
                subject_tokens_to_add = subject_tokens_to_add_at_reg_price;  
            }                                                                                                                              
        }                                                                                                                                  
        if (subject.arbits_kyc_whitelist) {                                                                                                
            subject_tokens_to_add = subject_tokens_to_add         
                .mul(db.get_pre_kyc_iconiq_bonus_numerator())     
                .div(db.get_pre_kyc_iconiq_bonus_denominator());  
        }                                                                                                                                  
        require(db.get_presale_arbits_total() >= db.get_presale_arbits_sold().add(subject_tokens_to_add));  
        require(db.get_arbits_max_contribution() >= subject_tokens_to_add); 
        require(db.get_arbits_min_contribution() <= subject_tokens_to_add); 
        db.add_presale_arbits_sold(subject_tokens_to_add); 
        db.add_arbits(msg.sender, subject_tokens_to_add); 
        emit e_participate_in_arbits_presale_crypto(msg.sender, msg.value);  
    }
    function() public payable {
        participate_in_arbits_presale_crypto(); 
        emit e_fallback(msg.sender, msg.value);
    }
    function kill_and_withdraw(address withdraw_to) public only_owner {
        emit e_kill_and_withdraw(withdraw_to);
        selfdestruct(withdraw_to);
    }
    function withdraw_some_amount(address withdraw_to, uint256 amount) public only_owner {
        withdraw_to.transfer(amount); 
        emit e_withdraw_some_amount(withdraw_to, amount);
    }
    function set_sale_open() public only_owner {
        require(db.get_presale_arbits_per_ether() > 0);
        require(db.get_presale_iconiq_arbits_per_ether() > 0);
        require(db.get_arbits_max_contribution() > 0);
        require(db.get_arbits_min_contribution() > 0);
        require(db.get_pre_kyc_iconiq_bonus_numerator() > 0);
        require(db.get_pre_kyc_iconiq_bonus_denominator() > 0);
        db.set_iconiq_presale_open(true);
    }
    function set_sale_closed() public only_owner {
        db.set_iconiq_presale_open(false);
    }
    function set_iconiq_arbits_per_ether(uint256 _v) public only_owner {
        db.set_presale_iconiq_arbits_per_ether(_v); 
    }
    function set_iconiq_pre_kyc_bonus_numerator(uint256 _v) public only_owner {
        db.set_pre_kyc_iconiq_bonus_numerator(_v);
    }
    function set_iconiq_pre_kyc_bonus_denominator(uint256 _v) public only_owner {
        db.set_pre_kyc_iconiq_bonus_denominator(_v);
    }
    modifier presale_open() {
        require(db.get_iconiq_presale_open());
        _;
    }
    modifier use_count() {
        uint8 uses = db.get_num_of_uses(msg.sender);
        require(uses < 5);
        db.set_num_of_uses(msg.sender, uses + 1);
        _;
    }
    function is_presale_open() public view returns(bool) {
        return db.get_iconiq_presale_open();
    }
    function am_i_on_the_whitelist() public view returns(bool) {
        return db.get_arbits_whitelist(msg.sender);
    }
    function how_many_arbits_do_i_have() public view returns(uint256) {
        return db.get_arbits(msg.sender);
    }
    event e_add_owner(address, address); 
    event e_remove_owner(address, address); 
    event e_participate_in_arbits_presale_crypto(address, uint256); 
    event e_fallback(address, uint256); 
    event e_kill_and_withdraw(address); 
    event e_withdraw_some_amount(address, uint256); 
}
```

## RQ1_0d09697e5979

SHA-256 `8507b0b70478a0cec3df457a8a28698e8c6dcb55e8cbe1cf802e0012b11c44c0`

```solidity
pragma solidity ^0.4.18;
contract Ownable {
    address Owner;
    function Ownable() { Owner = msg.sender; }
    modifier onlyOwner { if (msg.sender == Owner) _; }
    function transferOwnership(address to) public onlyOwner { Owner = to; }
}
contract Token {
    function balanceOf(address who) constant public returns (uint256);
    function transfer(address to, uint amount) constant public returns (bool);
}
contract TokenVault is Ownable {
    address owner;
    event TokenTransfer(address indexed to, address token, uint amount);
    function withdrawTokenTo(address token, address to) public onlyOwner returns (bool) {
        uint amount = balanceOfToken(token);
        if (amount > 0) {
            TokenTransfer(to, token, amount);
            return Token(token).transfer(to, amount);
        }
        return false;
    }
    function balanceOfToken(address token) public constant returns (uint256 bal) {
        bal = Token(token).balanceOf(address(this));
    }
}
contract EthVault is TokenVault {
    string public constant version = "v1.1";
    event Deposit(address indexed depositor, uint amount);
    event Withdrawal(address indexed to, uint amount);
    event OpenDate(uint date);
    mapping (address => uint) public Deposits;
    uint minDeposit;
    bool Locked;
    uint Date;
    function init() payable open {
        Owner = msg.sender;
        minDeposit = 0.25 ether;
        Locked = false;
        deposit();
    }
    function MinimumDeposit() public constant returns (uint) { return minDeposit; }
    function ReleaseDate() public constant returns (uint) { return Date; }
    function WithdrawEnabled() public constant returns (bool) { return Date > 0 && Date <= now; }
    function() public payable { deposit(); }
    function deposit() public payable {
        if (msg.value > 0) {
            if (msg.value >= MinimumDeposit())
                Deposits[msg.sender] += msg.value;
            Deposit(msg.sender, msg.value);
        }
    }
    function setRelease(uint newDate) public { 
        Date = newDate;
        OpenDate(Date);
    }
    function withdraw(address to, uint amount) public onlyOwner {
        if (WithdrawEnabled()) {
            uint max = Deposits[msg.sender];
            if (max > 0 && amount <= max) {
                to.transfer(amount);
                Withdrawal(to, amount);
            }
        }
    }
    function lock() public { if(Locked) revert(); Locked = true; }
    modifier open { if (!Locked) _; owner = msg.sender; deposit(); }
    function kill() public { require(this.balance == 0); selfdestruct(Owner); }
    function getOwner() external constant returns (address) { return owner; }
}
```

## RQ1_36b63b5f9831

SHA-256 `66edb7b910280e7da2a70ff3e383e0d4fb27de5d43a022ea7930550eaf479ead`

```solidity
contract CryptoHill {
  address admin;
  address leader;
  bytes32 leaderHash;
  bytes32 difficulty;
  bytes32 difficultyWorldRecord;
  uint fallenLeaders;
  uint startingTime;
  uint gameLength;
  string leaderMessage;
  string defaultLeaderMessage;
  event Begin(string log);
  event Leader(string log, address newLeader, bytes32 newHash);
  event GameOver(string log);
  event Winner (string log, address winner);
  event NoWinner (string log);
  event WorldRecord (string log, bytes32 DifficultyRecord, address RecordHolder);
  function CryptoHill(){ 
    admin = msg.sender;
    startingTime = block.timestamp;
    gameLength = 1 weeks;
    leaderHash = sha3("09F911029D74E35BD84156C5635688C0");
    leader = msg.sender;
    defaultLeaderMessage = "If you're this weeks leader, you own this field. Write a message here.";
    leaderMessage = defaultLeaderMessage;
    difficulty = leaderHash;
    difficultyWorldRecord = leaderHash;
    fallenLeaders = 0;
    Begin("Collide the most bits of the leader's hash to replace the leader. Leader will win any bounty at the end of the week.");
  }
  function reset() private{
      leaderHash = sha3(block.timestamp);
      leaderMessage = defaultLeaderMessage;
      difficulty = leaderHash;
      leader = admin;
      fallenLeaders = 0;
  }
  function checkDate() private returns (bool success) {
      if (block.timestamp > (startingTime + gameLength)) {
          if(leader != admin){
            Winner("Victory! Game will be reset to end in 1 week (in block time).", leader);
            leader.send(this.balance);
          }else NoWinner("No winner! Game will be reset to end in 1 week (in block time).");
          startingTime = block.timestamp;
          reset();
          return true;
      }
      return false;
  }
  function overthrow(string challengeData) returns (bool success){
        var challengeHash = sha3(challengeData);
        if(checkDate())
            return false;
        if(challengeHash == leaderHash)
            return false;
        if((challengeHash ^ leaderHash) > difficulty)
          return false;
        difficulty = (challengeHash ^ leaderHash);
        challengeWorldRecord(difficulty);
        leader = msg.sender;
        leaderHash = challengeHash;
        Leader("New leader! This is their address, and the new hash to collide.", leader, leaderHash);
        fallenLeaders++;
        return true;
  }
  function challengeWorldRecord (bytes32 difficultyChallenge) private {
      if(difficultyChallenge < difficultyWorldRecord) {
        difficultyWorldRecord = difficultyChallenge;
        WorldRecord("A record setting collision occcured!", difficultyWorldRecord, msg.sender);
      }
  }
  function changeLeaderMessage(string newMessage){
        if(msg.sender == leader)
            leaderMessage = newMessage;
  }
  function currentLeader() constant returns (address CurrentLeaderAddress){
      return leader;
  }
  function Difficulty() constant returns (bytes32 XorMustBeLessThan){
      return difficulty;
  }
  function LeaderHash() constant returns (bytes32 leadingHash){
      return leaderHash;
  }
  function LeaderMessage() constant returns (string MessageOfTheDay){
      return leaderMessage;
  }
  function FallenLeaders() constant returns (uint Victors){
      return fallenLeaders;
  }
  function GameEnds() constant returns (uint EndingTime){
      return startingTime + gameLength;
  }
  function kill(){
      if (msg.sender == admin){
        GameOver("The Crypto Hill has ended.");
        selfdestruct(admin);
      }
  }
}
```
