# ncpeek

`ncpeek` is a netconf client that retrieves telemetry data using netconf, it uses the `ncclient` library.

To use it, install the dependencies needed

```bash
poetry install
peotry shell
```

If you use `vscode`, start `poetry shell` and then start vscode with `code .`

## Usage

You can use in two ways `ncpeek`; cli or api.

### CLI

```bash
❯ python ncpeek/client.py

usage: client.py [-h] [-d DEVICE_SETTINGS]
                 (-x XML_FILTER | -p XPATH_FILTER)

Netconf client to gather data from devices. The client
can be used via CLI or API. Provide device credentials
and options via a json file. User must specify if an XML
filter or XPath is to be used. Note that only one can be
used.

options:
  -h, --help            show this help message and exit
  -d DEVICE_SETTINGS, --device-settings DEVICE_SETTINGS
                        Device Settings in json format.
                        See examples under ncpeek/devices
  -x XML_FILTER, --xml-filter XML_FILTER
                        Netconf Filter to apply in XML
                        format. See examples under
                        ncpeek/filters
  -p XPATH_FILTER, --xpath-filter XPATH_FILTER
                        Netconf Filter to apply in XPath.
                        Formats: <xpath> OR
                        <namespace>:<xpath> Example:
                        'interfaces/interface' OR
                        'http://cisco.com/ns/yang/Cisco-
                        IOS-XE-interfaces-
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

## Built-in data

`ncpeek` has some data already on it, so you can test it rigth away via CLI or API

### Device Settings

`ncpeek` expects the device settings under a specific structure.

- **CLI:** you can pass the json file containing the settings.

- **API:** besided the json file, you can pass a string with valid json or a python dictionary with the same structure.

You can add multiple devices under one json array, however the data is retrieve sequencially.

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

The `ncpeek/devices` directory is the default directory for `ncpeek` to look for the device settings. To use other directories to place your device settings, pass the relative or absolute path to `ncpeek`.

### XML filters

## Operations

Currently only uses the [GET operation](ncpeek/netconf_session.py#L34) to retrieve data.

## Ways to retrieve data

Relative and absolute paths are supported to define device or filters files.

### Define your devices

Under the [devices directory](devices) create a json file. Follow the structure defined of the existing files. **Don't add or remove fields,** these are used to [build a netconf_device object](netconf_devices.py)

### xml filter

You need to specify an `xml` file with the filter you want to use and the `--xml_filter` option when calling the script.

For example:

- `--xml_filter=cisco_xe_ietf-interfaces.xml`

The script supports relative and absolute paths. Default directory is [the filter directory](filters), place your `xml` files there if you don't want to deal with absolute or relative paths.

### xpath

`xpath` can be use with the following formats:

- `--xpath_filter=<xpath>`
- `--xpath_filter=<namespace>:<xpath>`

For example:

```bash
--xpath_filter=interfaces/interface
--xpath_filter=http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper:interfaces/interface
```

The `xpath` filter is used as [ID internally](factory.py#L21).

## Netconf Filters

At the time of writting it parses the output of the following netconf filters:

- `ietf-interfaces`
- `Cisco-IOS-XE-interfaces-oper`
- `Cisco-IOS-XE-memory-oper`
- `Cisco-IOS-XE-isis-oper`

If using the `--xml_filter` option, you can find the xml used under [the filter directory.](filters)

The python code that parses the RPC reply is found under [the parsers directory](parsers)

## Adding a Parser

If you want to add your own parser. You need to:

- Create a parser under [the parsers directory](parsers)
  - You parser must implement the `Parser` class. See an [existing parser for an example](parsers/cisco_ios_xe_memory_oper.py#L8)
- Add your new parser to [the factory file](factory.py#L5) under the match statement.
  - If using a `xml` file, use the file name as ID, including the `.xml` extension.
  - If using `xpath`, use the whole xpath expression.
