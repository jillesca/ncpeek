# ncpeek

`ncpeek` (short for `netconf peek`) is a netconf client that retrieves data using the `ncclient` library.

It parses the rpc-reply into json format by default, removing any namespaces.[^1] Additional data as such as `ip`, `device` and `field` are also included in the output.

Here's an example on how `ncpeek` works, using the following xml filter:

```xml
<filter>
  <system xmlns="http://openconfig.net/yang/system">
    <state>
      <hostname />
    </state>
  </system>
</filter>
```

It will yield this result.

```json
[
  {
    "ip": "sandbox-iosxr-1.cisco.com",
    "device": "sandbox-iosxr-1.cisco.com",
    "field": "generic",
    "data": {
      "system": {
        "state": {
          "hostname": "sandbox-iosxr"
        }
      }
    }
  }
]
```

For more complex data manipulation or logic, you can add a custom parser for your xml filter or xpath. See [Adding a Parser](#adding-a-parser) for instructions.

## Use cases

I developed originally `ncpeek` to be used within [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) to gather telemetry data from network devices and print the metrics. This was showcased in a [demo presented at Cisco Impact 2023.](https://github.com/jillesca/open_telemetry_network_impact) In this scenario, a CLI client with a simple interface was what I needed.

For an upcoming talk I will deliver at Cisco Live Amsterdam 2024, I improved the netconf client and added an API layer. This allows other systems, such as AI, to call `ncpeek` and fetch data from network devices. For this use case, I needed a simple API for the AI to use.

### State

It's important to note upfront that `ncpeek` is a pet project primarily used for demos. So far, testing has been limited to C8000V 17.09.02a and IOSXR 7.3.2 running on the DevNet always-on sandbox.

PRs are welcome, but the support provided might be limited due to the nature of the project. If you have specific requirements or need extensive modifications, you might find it more efficient to fork the project.

See the file [Contributing](CONTRIBUTING.md) for more information.

## Installation

For CLI or API you can install `ncpeek` via pip. [See Details on pypi.](https://pypi.org/project/ncpeek/)

```bash
 pip install ncpeek
```

To add a custom parser or work directly with the code [see Development.](#development)

> `ncpeek` was developed on Python 3.11, consider using a virtual or dedicated environment when use it.

## Usage

There are two ways to use `ncpeek`; via the command-line interface (CLI) or through the API. Note that filters can be either `xml` or `xpath`, but only one type can be used at a time.

### CLI

```bash
❯ python -m ncpeek
usage: __main__.py [-h] [-d DEVICE_SETTINGS] (-x XML_FILTER | -p XPATH_FILTER)

'ncpeek' is a netconf client designed to fetch data from various devices.
The client can be utilized in two distinct ways,
either via Command Line Interface (CLI) or Application Programming Interface (API).
The data retrieval can be filtered through either XML or XPath,
however, only one filter type can be applied at a given time.
Note that in CLI mode, only filenames can be treated as arguments.
Source code: https://github.com/jillesca/ncpeek

options:
  -h, --help            show this help message and exit
  -d DEVICE_SETTINGS, --device-settings DEVICE_SETTINGS
                        Specify JSON filename containing device settings.
                        Visit https://github.com/jillesca/ncpeek/tree/main/ncpeek/devices for examples.
  -x XML_FILTER, --xml-filter XML_FILTER
                        Specify XML filename containing XML filter.
                        Visit https://github.com/jillesca/ncpeek/tree/main/ncpeek/filters for more details.
  -p XPATH_FILTER, --xpath-filter XPATH_FILTER
                        Formats: <xpath> OR <namespace>:<xpath>
                        Example: 'interfaces/interface' OR
                        'http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper:interfaces/interface'
```

Here's an example of how to use `ncpeek` with a specific device setting and xml filter:

```bash
python -m ncpeek --device-settings=devnet_xe_sandbox.json --xml-filter=Cisco-IOS-XE-memory-oper.xml
```

Or with a specific device setting and xpath filter:

```bash
python -m ncpeek --device-settings=devnet_xe_sandbox.json --xpath-filter=http://cisco.com/ns/yang/Cisco-IOS-XE-native:/native/hostname
```

`ncpeek` will print the data retrieved from the network device to stdout.

### API

```python
from ncpeek.client import NetconfClient

def api_call() -> None:
    """Example NetconfClient API"""
    client = NetconfClient()
    client.set_devices_settings(xr_device_settings)
    client.set_xml_filter(xml_filter)
    try:
        result = client.fetch()
    except Exception as err:
        result = [{"error": f"{err=}"}]
    print(result)
```

`ncpeek` will return the data as json. See [api_example.py](examples/api_example.py) for the full example.

## Device Settings

The device settings should follow a specific structure.

- **CLI:** json filename containing the device settings.

  ```bash
  --device-settings=devnet_xe_sandbox.json
  ```

- **API:** json filename, valid json string or a python dictionary with the same structure. Use the [`set_devices_settings`](ncpeek/client.py#L27) method.

  ```python
  def set_devices_settings(
          self, device_settings: Union[list, str]
      ) -> None:
  ```

The **required** fields are:

- `host`
- `username`
- `password`

The rest of the fields take defaults on [netconf_device](ncpeek/netconf_devices.py#L6)

Here, you can find an example of the device settings.

```json
[
  {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "port": 830,
    "username": "admin",
    "password": "C1sco12345",
    "hostkey_verify": "False",
    "timeout": 10,
    "device_params": {
      "name": "iosxe"
    }
  }
]
```

You can add multiple devices in a single json array. However, please note that the data is retrieved sequencially.

See examples on [ncpeek/devices](ncpeek/devices/)

## Filters

### XML

- **CLI.** filename with the xml filter.

  ```python
  --xml-filter=cisco_xe_ietf-interfaces.xml
  ```

  - See examples on [ncpeek/filters](ncpeek/filters/)

- **API.** filename or xml string. Use the [`set_xml_filter`](ncpeek/client.py#L38) method.

  ```python
    def set_xml_filter(self, xml_filter: str) -> None:
  ```

### xpath

The following formats are accepted:

```bash
<xpath>
<namespace>:<xpath>
```

- **CLI.** `xpath` string.

  - Examples:

    ```bash
    --xpath-filter=interfaces/interface
    ```

    ```bash
    --xpath-filter=http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper:interfaces/interface
    ```

- **API.** `xpath` string. Use the [`set_xpath_filter`](ncpeek/client.py#L46) method.

  ```python
    def set_xpath_filter(self, xpath_filter: str) -> None:
  ```

## Operations

Currently, `ncpeek` only uses the [GET operation](ncpeek/netconf_session.py#L34) to retrieve data. More operations may be added in future versions.

### Built-in filters and parsers

You can call directly any of these filters by its name, without specifying their path.

Use the [devnet sandbox](ncpeek/devices/) for testing.

- [xml filters built-in](ncpeek/filters/):

  - `cisco_xe_ietf-interfaces.xml` (custom parser added)
  - `Cisco-IOS-XE-interfaces-oper.xml` (custom parser added)
  - `Cisco-IOS-XE-memory-oper.xml` (custom parser added)
  - `Cisco-IOS-XR-facts.xml`
  - `Cisco-IOS-XR-hostname.xml`

- xpath parser built-in
  - `http://cisco.com/ns/yang/Cisco-IOS-XE-isis-oper:/isis-oper-data/isis-instance` (custom parser added)

## Development

To Install the dependencies needed, use these commands.

```bash
poetry install
```

```bash
peotry shell
```

> If you use `vscode`, start `poetry shell` and then start vscode with `code .`

In case you don't have poetry, install it with `curl -sSL https://install.python-poetry.org | python3 -`

If you want to use pip, install the dependencies manually. The only requirement is **paramiko <=2.8.1** for working with older XR and Junos versions.

If you ran into module import problems, add the root project to your `PYHTONPATH`

```bash
export PYTHONPATH=.
```

### Default directories

- Device Settings default directory is [ncpeek/devices](ncpeek/devices/).
- XML Filters default directory is [ncpeek/filters](ncpeek/filters).

### Adding a Parser

To add a custom parser follow the steps below:

1. Clone this repository.
2. Create a parser under [the parsers directory](ncpeek/parsers)

   1. Your custom parser must implement the `Parser` class. See an [existing parser for an example](ncpeek/parsers/cisco_ios_xe_memory_oper.py#L8)

   2. the `parse` function must take three arguments and return a list with a dictionary inside.

      ```python
      def parse(
        self,
        data_to_parse: dict,
        device: NetconfDevice,
        netconf_filter_id: str,
      ) -> list[dict]:
      ```

   3. The variable `data_to_parse` holds a dictionary with **data** as key, and the rpc-reply as the value.

      ```python
      {
          "data": {
              "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
              "@xmlns:nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
              "memory-statistics": {
                  "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper",
                  "memory-statistic": [
                      {
                          "name": "Processor",
                          "total-memory": "2028113884",
                          "used-memory": "192040880",
                      },
                  ],
              },
          }
      }
      ```

   > Review the [tests for the parsers](ncpeek/tests/test_parsers/) to get more familiar.

   4. Is recommended to return the following fields beside the data on your parser

      ```python
        "field": self.netconf_filter_id,
        "device": self.device.hostname,
        "ip": self.device.host,
      ```

3. Add your new parser to [the factory mapping.](ncpeek/factory/factory_mappings.py#L12) This way, `ncpeek` knows which parser to use for which filter.

   1. Follow the dictionary structure, where the first keys are the name of the filter you are using.

      1. If using a `xml` file, use the filename as ID, including the `.xml` extension.
      2. If using `xpath`, use the whole xpath expression.

   2. On the second level of the dictionary, add the module that has your parser and the class to import.

      ```python
      PARSER_MAPPING: Dict[str, Dict[str, str]] = {
          "cisco_xe_ietf-interfaces.xml": {
              "module": "ncpeek.parsers.cisco_xe_ietf_interfaces",
              "class": "InterfaceStatsIETF_IOSXEParser",
          },
          "http://cisco.com/ns/yang/Cisco-IOS-XE-isis-oper:/isis-oper-data/isis-instance": {
              "module": "ncpeek.parsers.cisco_ios_xe_isis_oper",
              "class": "ISISStatsIOSXEParser",
          },
      }
      ```

## FAQ

- Why I see a deprecation message?
  - Unfortunately, paramiko >=2.9 and IOS-XR 7.3.2 don't go well together, so I had to use an old paramiko <=2.8.1 which has this deprecation message. See [ncclient/issues/526](https://github.com/ncclient/ncclient/issues/526#issuecomment-1868278440) for more info.

[^1]: Up to a maximum of 10 nested dictionaries. After that, all remaining nested directionaries will be return as they are. This [limit can be configured](ncpeek/parsers/remove_namespaces.py#L12) per custom parser.
