# slack_differ
a python script that sends messages to a slack webhook when the output from a script changes

## what it does
The script looks for files ending with .json inside a scripts dir. It executes them and records their stdout. If the output has changed it pushes to a configured slack webhook. 

## how to get started
1. run `slack_differ example`
2. `chmod +x` the example.sh it produces under the new scripts dir
3. change the configuration in `scripts/example.json` to match your webhook url

## example configuration json
```json
{  
  "script":"example.sh",
  "title":"script title",
  "user":"examplebot",
  "slack_url":"https://hook.slack.com/XXX/YYY",
  "channel":"#example",
  "emoji":":metal:"
}
```
