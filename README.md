# Slack Snooper
Automatically sets your Slack status based on your connected WiFi.

## Installation (OS X only)
1. Create a config.json that tells the script what status to set when connected to which WiFi networks (see config.json.example as an example)

2. Add a `launchd` script that will watch relevant files when your connected SSID changes and execute the script. Create an xml file at
`~/Library/LaunchAgents/local.slacksnooper.plist`:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>local.slackstatus</string>

  <key>LowPriorityIO</key>
  <true/>

  <key>WorkingDirectory</key>
  <string>YOUR-SLACK-SNOOPER-INSTALL-DIR</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>TOKEN</key>
    <string>YOUR-SUPERSECRET-SLACK-TOKEN</string>
  </dict>


  <key>ProgramArguments</key>
  <array>
      <string>/usr/local/bin/python</string>
      <string>slack_snooper.py</string>
  </array>

  <key>StandardErrorPath</key>
  <string>/tmp/slack-snooper.err</string>
  <key>StandardOutPath</key>
  <string>/tmp/slack-snooper.out</string>

  <key>WatchPaths</key>
  <array>
    <string>/etc/resolv.conf</string>
    <string>/Library/Preferences/SystemConfiguration/NetworkInterfaces.plist</string>
    <string>/Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist</string>
  </array>

  <key>RunAtLoad</key>
  <true/>
</dict>
</plist>
```

Make sure you replace `YOUR-SLACK-SNOOPER-INSTALL-DIR` and `YOUR-SUPERSECRET-SLACK-TOKEN` appropriately.

3. Next, load it using:
```
sudo launchctl load ~/Library/LaunchAgents/local.slacksnooper.plist
```

And that's it!
