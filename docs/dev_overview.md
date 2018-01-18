# µRaiden

µRaiden components overview.

 * [HTTP Request and Response Headers](#http-request-and-response-headers)
 * [Exceptions](#exceptions)
 * [Off-Chain Micropayment Sequence](#off-chain-micropayment-sequence)
 * [Proxy](#proxy)
 * [Python Client](#python-client)
 * [Web Client](#web-client)
 * [Smart Contract](#smart-contract)

## HTTP Request and Response Headers

Encoding:
 * `address`	`0x` prefixed hex encoded
 * `uint`	`[0-9]`
 * `bytes`	`0x` prefixed hex encoded


### Response Headers






#### 200 OK


|        Headers        |   Type   |   Description                              |
| --------------------- | -------- | ------------------------------------------ |
|  RDN-Gateway-Path     | bytes    |  Path root of the channel management app   |
|  RDN-Receiver-Address | address  |  Address of the Merchant                   |
|  RDN-Contract-Address | address  |  Address of RaidenMicroTransferChannels  contract |
|  RDN-Token-Address    | address  |  Address of the Token contract             |
|  RDN-PRICE            | uint     |  Resource price                            |
|  RDN-Sender-Address   | address  |  Address of the Client                     |
|  RDN-Sender-Balance   | uint     |  Balance of the Channel                    |



#### 402 Payment Required



|        Headers        |   Type   |   Description                              |
| --------------------- | -------- | ------------------------------------------ |
|  RDN-Gateway-Path     | bytes    |  Path root of the channel management app   |
|  RDN-Receiver-Address | address  |  Address of the Merchant                   |
|  RDN-Contract-Address | address  |  Address of RaidenMicroTransferChannels  contract |
|  RDN-Token-Address    | address  |  Address of the Token contract             |
|  RDN-PRICE            | uint     |  Resource price                            |
| RDN-Balance-Signature | bytes    |  Optional. Last saved balance proof from the sender. |
|  |  | __+ one of the following:__ |
| RDN-Insufficient-Confirmations | string |  Failure - not enough confirmations after the channel creation. Client should wait and retry. |
| RDN-Nonexisting-Channel | string |  Failure - channel does not exist or was closed. |
| RDN-Invalid-Balance-Proof  | uint |  Failure - Balance must not be greater than deposit or The balance must not decrease. |
| RDN-Insufficient-Funds          | uint     |  Failure - either Payment value too low or balance exceeds deposit|
| RDN-Invalid-Amount  | uint     |  Failure - wrong payment value |


#### 409

- ValueError



#### 502

- Ethereum node is not responding
- Channel manager ETH balance is below limit



### Request Headers



|        Headers        |   Type   |   Description                              |
| --------------------- | -------- | ------------------------------------------ |
| RDN-Contract-Address  | address  |  Address of RaidenMicroTransferChannels  contract |
| RDN-Receiver-Address  | address  |  Address of the Merchant                   |
| RDN-Sender-Address    | address  |  Address of the Client                     |
| RDN-Payment           | uint     |  Amount of the payment                     |
| RDN-Sender-Balance    | uint     |  Balance of the Channel                    |
| RDN-Balance-Signature | bytes    |  Signature from the Sender, signing the balance (post payment) |
| RDN-Open-Block        | uint     |  Opening block number of the channel required for unique identification |



## Exceptions



https://github.com/raiden-network/microraiden/blob/master/microraiden/microraiden/exceptions.py



## Off-Chain Micropayment Sequence


(not-so-standard sequence diagram)
For a better overview, also check out how the smart contract does a transfer validation:  [/contracts/README.md#generating-and-validating-a-transfer](/contracts/README.md#generating-and-validating-a-transfer)

![](/docs/diagrams/OffChainSequence.png)



## µRaiden Server

Non-detailed components overview. For function arguments and types, please check source code and docstrings.


### Channel manager

![](/docs/diagrams/ChannelManagerClass.png)


### Proxy


![](/docs/diagrams/ProxyClass.png)


## Python Client

![](/docs/diagrams/PythonClientClass.png)


## Web Client

[/microraiden/microraiden/webui/microraiden/README.md](/microraiden/microraiden/webui/microraiden/README.md)


## Smart Contract

[/contracts/README.md](/contracts/README.md)
