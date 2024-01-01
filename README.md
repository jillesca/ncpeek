# ncpeek

`ncpeek` (short for `netconf peek`) is a netconf client that retrieves telemetry data using netconf, it uses the `ncclient` library.

By default it will parse the rpc-reply into json removing any namespaces under the `data` key. It will add some add some additional data as such as `ip`, `device` and `field`.

For example, using the following xml filter below

```xml
<filter>
  <system xmlns="http://openconfig.net/yang/system">
    <state>
      <hostname />
    </state>
  </system>
</filter>
```

Will yield this result.

```json
[
  {
    "ip": "sandbox-iosxr-1.cisco.com",
    "device": "sandbox-iosxr-1.cisco.com",
    "field": "generic",
    "data": { "system": { "state": { "hostname": "sandbox-iosxr" } } }
  }
]
```

If you need to manipulate the shape of the data or add some logic, you can add a custom parser for your xml filter or xpath. See [Adding a Parser](#adding-a-parser) for instructions.

## Usage

You can use in two ways `ncpeek`; cli or api.

> filters can be `xml` or `xpath`, but only one can be used at a time.

### CLI

```bash
❯ python ncpeek/client.py

usage: client.py [-h] [-d DEVICE_SETTINGS] (-x XML_FILTER | -p XPATH_FILTER)

Netconf client to gather data from devices. The client can be used via CLI or API. Provide
device credentials and options via a json file. User must specify if an XML filter or
XPath is to be used. Note that only one can be used.

options:
  -h, --help            show this help message and exit
  -d DEVICE_SETTINGS, --device-settings DEVICE_SETTINGS
                        Device Settings in json format. See examples under ncpeek/devices
  -x XML_FILTER, --xml-filter XML_FILTER
                        Netconf Filter to apply in XML format. See examples under
                        ncpeek/filters
  -p XPATH_FILTER, --xpath-filter XPATH_FILTER
                        Netconf Filter to apply in XPath. Formats: <xpath> OR
                        <namespace>:<xpath> Example: 'interfaces/interface' OR
                        'http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-
                        oper:interfaces/interface'
```

For example:

```bash
python ncpeek/client.py --device-settings=devnet_xe_sandbox.json --xml-filter=Cisco-IOS-XE-memory-oper.xml
```

```bash
python ncpeek/client.py --device-settings=devnet_xe_sandbox.json --xpath-filter=http://cisco.com/ns/yang/Cisco-IOS-XE-native:/native/hostname
```

`ncpeek` will then print to stdout the data retrieve from the network device.

### API

```python
from ncpeek.client import NetconfClient

def api_call() -> None:
    """Example NetconfClient API"""
    result = []
    client = NetconfClient()
    client.set_devices_settings(xr_device_settings)
    client.set_xml_filter(xml_filter)
    try:
        result = client.run()
    except Exception as err:
        result.append({"error": f"{err=}"})
    print(result)
```

`ncpeek` will return the data as json.

See [api_example.py](examples/api_example.py) for the full example.

## Device Settings

`ncpeek` expects the device settings under a specific structure.

- **CLI:** json filename containing the device settings.

- **API:** json filename, valid json or a python dictionary with the same structure.

You can add multiple devices under one json array, however the data is retrieved sequencially.

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

Under `ncpeek/devices` you can find two examples, [devnet_xe_sandbox.json](ncpeek/devices/devnet_xe_sandbox.json) and [devnet_xr_sandbox.json](ncpeek/devices/devnet_xr_sandbox.json).

> Default directory is [ncpeek/devices](ncpeek/devices/) for `ncpeek` to look for the device settings. To use other directories, add the relative or absolute path to the filename.

## Filters

> Default directory is [ncpeek/filters](ncpeek/filters). To use other directories for your filters, add the relative or absolute path to the filename.

### XML

- **CLI.** filename with the xml filter.

  ```python
  --xml_filter=cisco_xe_ietf-interfaces.xml
  ```

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
    --xpath_filter=interfaces/interface
    ```

    ```bash
    --xpath_filter=http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper:interfaces/interface
    ```

- **API.** `xpath` string. Use the [`set_xpath_filter`](ncpeek/client.py#L46) method.

  ```python
    def set_xpath_filter(self, xpath_filter: str) -> None:
  ```

## Operations

Currently only uses the [GET operation](ncpeek/netconf_session.py#L34) to retrieve data. As time goes, more operations could be added.

### Built-in filters and parsers

You can call directly any of these filters using the [devnet sandbox.](ncpeek/devices/)

- xml filters built-in:

  - cisco_xe_ietf-interfaces.xml (custom parser added)
  - Cisco-IOS-XE-interfaces-oper.xml (custom parser added)
  - Cisco-IOS-XE-memory-oper.xml (custom parser added)
  - Cisco-IOS-XR-facts.xml
  - Cisco-IOS-XR-hostname.xml

- xpath parser built-in
  - `http://cisco.com/ns/yang/Cisco-IOS-XE-isis-oper:/isis-oper-data/isis-instance` (custom parser added)

## Development

Install the dependencies needed

```bash
poetry install
```

```bash
peotry shell
```

If you use `vscode`, start `poetry shell` and then start vscode with `code .`

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

   4. Review the [tests for the parsers](ncpeek/tests/test_parsers/) to get more familiar.

   5. Is recommended to return the following fields beside the data on your parser

      ```python
        "field": self.netconf_filter_id,
        "device": self.device.host,
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
