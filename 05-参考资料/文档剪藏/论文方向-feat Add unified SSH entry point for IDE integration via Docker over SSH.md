---
title: "feat: Add unified SSH entry point for IDE integration via Docker over SSH"
source: "https://www.devstar.cn/devstar/devstar/pulls/108#issuecomment-2175"
author:
  - "[[devstar]]"
published:
created: 2026-03-20
description: "devstar - DevStar Studio"
tags:
  - "clippings"
---
## PR: Unified SSH Entry Point for "Open with VSCode" Feature

---

## Description

### Background & Problem

Currently, the "Open with VSCode" feature requires each DevContainer to expose its own SSH port. When a user clicks "Open with VSCode", the system:

1. Gets the container's mapped SSH port (e.g., 32768, 32769, etc.)
2. Generates a URL like `vscode://mengning.devstar/openProject?port=32768...`
3. VSCode uses Remote-SSH to connect to that specific port

**Problems with this approach:**

- Each container needs to run its own SSH server
- Dynamic port allocation is complex to manage
- Firewall rules become complicated with many ports
- Port conflicts can occur

**Goal:** Use a single SSH entry point (port 2222) for all containers, eliminating per-container SSH ports.

---

## Solution Exploration Journey

We tried 4 different approaches before finding a working solution:

### Approach 1: Remote-SSH to DevStar Main Container

**Idea:** SSH into the DevStar main container (port 2222), then use Dev Containers to attach to user containers.

**Implementation tried:**

```markup
vscode://vscode-remote/ssh-remote+devstar-host/workspace/project
```

**Why it failed:**

- DevStar main container is based on **Alpine Linux**
- VS Code Server requires **glibc**, but Alpine uses **musl libc**
- Official Microsoft documentation confirms: "Remote-SSH does NOT support Alpine Linux"
- Reference: [https://code.visualstudio.com/docs/remote/linux](https://code.visualstudio.com/docs/remote/linux)

**Error observed:**

```markup
/root/.vscode-server/bin/.../node: not found
```

---

### Approach 2: Dynamic devcontainer.json Generation

**Idea:** Generate `devcontainer.json` pointing to existing container, let Dev Containers extension attach to it.

**Implementation tried:**  
Created files on server:

```json
// .devcontainer/devcontainer.json
{
  "name": "Attach to Container",
  "dockerComposeFile": "docker-compose.yml",
  "service": "devcontainer",
  "workspaceFolder": "/workspace/project"
}

// .devcontainer/docker-compose.yml
services:
  devcontainer:
    container_name: "user-project-container"
    image: ubuntu:latest
```

**Why it failed:**

- Dev Containers extension always tries to **CREATE** new containers via docker-compose
- It doesn't attach to existing containers with the same name
- Error: `The container name "/user-project-container" is already in use`

---

### Approach 3: attached-container URI Scheme

**Idea:** Use VSCode's built-in `attached-container` URI to directly attach to a container.

**Implementation tried:**

```javascript
// Container config
const config = { containerName: "user-project-container" };
const hex = Buffer.from(JSON.stringify(config)).toString('hex');
const uri = \`vscode://vscode-remote/attached-container+${hex}/workspace\`;
```

**Variations tested:**

1. Simple containerName only
2. With `dockerContext` parameter
3. With `dockerHost` in config
4. With `settings.docker.host` in config
5. With `DOCKER_HOST` environment variable

**Why ALL failed:**

- The `attached-container` URI scheme **ignores** all docker.host configurations
- It always tries to connect to **local** Docker daemon
- Error: `Cannot attach to the container with name/id xxx, it no longer exists`

**Key finding from logs:**

```markup
// When using command (works):
[13 ms] Context: devstar-remote  ← Uses configured context

// When using URI (fails):
[21 ms] Setting up container: xxx
[25 ms] Start: Run: docker inspect --type container xxx  ← No context, uses local
```

---

### Approach 4: Docker over SSH + attachToRunningContainer Command

**Final working solution!**

**Key Discovery:**  
By reverse-engineering the Dev Containers extension source code, we found:

```javascript
// From extension.js
let g = async E => {
  let b = typeof E == "string" ? E : E?.containerDesc?.Id;
  if (b) {
    // Direct lookup by name/ID - no picker UI!
    x = await si(L, b)
  } else {
    // Show picker UI
    x = await hve(t, c.log, L)
  }
}
commands.registerCommand("remote-containers.attachToRunningContainer", g)
```

**The command accepts container name as parameter and reads docker.host setting!**

**Working flow:**

1. User configures `docker.host` in VSCode settings pointing to remote server
2. Extension calls `vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName)`
3. Dev Containers extension connects to remote Docker via SSH
4. Attaches directly to specified container

---

## Implementation Details

### Server-Side Changes (This PR)

#### 1\. New Configuration Options

**File: `modules/setting/devcontainer.go`**

```markup
// Added new config fields
type DevContainerConfigType struct {
    // ... existing fields ...
    SSHEnabled      bool   // Enable unified SSH entry
    SSHPort         int    // SSH port (default: 2222)
    SSHUser         string // SSH user (default: git)
    SSHWorkspacePath string // Workspace path on host
}
```

**Configuration in `app.ini`:**

```markup
[devcontainer]
SSH_ENABLED = true
SSH_PORT = 2222
SSH_USER = git
SSH_WORKSPACE_PATH = /var/lib/gitea/devstar-workspace
```

#### 2\. URL Template Updates

**File: `modules/setting/config.go`**

Added 3 new placeholders to IDE URL templates:

```markup
// Before
"vscode://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access_token={token}&devstar_username={devstar_username}&devstar_domain={domain}"

// After
"vscode://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access_token={token}&devstar_username={devstar_username}&devstar_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"
```

#### 3\. URL Generation Logic

**File: `services/devcontainer/devcontainer.go`**

Modified `Get_IDE_TerminalURL()` function:

```markup
func Get_IDE_TerminalURL(...) (string, error) {
    var port, hostname, username string

    if setting.DevContainerConfig.SSHEnabled {
        // Unified SSH mode: use configured port
        port = fmt.Sprintf("%d", setting.DevContainerConfig.SSHPort)
        hostname = setting.Domain
        username = setting.DevContainerConfig.SSHUser
    } else if setting.K8sConfig.Enable {
        // K8s mode: use NodePort
        port = fmt.Sprintf("%d", devcontainerApp.Status.NodePortAssigned)
        hostname = devContainerInfo.DevcontainerHost
        username = doer.Name
    } else {
        // Docker mode: use mapped port
        mappedPort, _ := docker_module.GetMappedPort(ctx, containerName, "22")
        port = fmt.Sprintf("%d", mappedPort)
        hostname = devContainerInfo.DevcontainerHost
        username = doer.Name
    }

    url := "://mengning.devstar/openProject?..." +
        "&hostname=" + hostname +
        "&port=" + port +
        "&username=" + username + "..."

    // Add unified SSH params
    if setting.DevContainerConfig.SSHEnabled {
        url += "&sshUnified=true"
        url += "&containerName=" + devContainerInfo.Name
        url += "&workspacePath=" + setting.DevContainerConfig.SSHWorkspacePath
    }

    return url, nil
}
```

#### 4\. Template Parameter Replacement

**File: `routers/web/devcontainer/devcontainer.go`**

Added new fields to `IDETemplateParams`:

```markup
type IDETemplateParams struct {
    // ... existing fields ...
    SSHUnified    string
    ContainerName string
    WorkspacePath string
}

func replaceIDETemplate(template string, params IDETemplateParams) string {
    // ... existing replacements ...
    result = strings.ReplaceAll(result, "{sshUnified}", params.SSHUnified)
    result = strings.ReplaceAll(result, "{containerName}", params.ContainerName)
    result = strings.ReplaceAll(result, "{workspacePath}", params.WorkspacePath)
    return result
}
```

#### 5\. Docker/SSH Setup

**File: `docker/Dockerfile.devstar`**

```dockerfile
# Ensure openssh is installed
RUN apk --no-cache add openssh openssh-keygen || true

# Install glibc (for potential future Alpine Remote-SSH support)
RUN apk --no-cache add --virtual .glibc-deps wget ca-certificates && \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r1/glibc-2.35-r1.apk && \
    apk add --no-cache --force-overwrite glibc-2.35-r1.apk && \
    rm glibc-2.35-r1.apk && \
    apk del .glibc-deps || echo "glibc installation optional"
```

**File: `docker/rootless/usr/local/bin/docker-setup.sh`**

```bash
# DevContainer SSH Setup (port 2222)
DEVCONTAINER_SSH_PORT=${DEVCONTAINER_SSH_PORT:-"2222"}

# Setup SSH directory and keys
mkdir -p ${HOME}/.ssh && chmod 700 ${HOME}/.ssh
ssh-keygen -A 2>/dev/null || true

# Create sshd config for port 2222
cat > /tmp/sshd_config_devcontainer << EOF
Port ${DEVCONTAINER_SSH_PORT}
ListenAddress 0.0.0.0
PubkeyAuthentication yes
PasswordAuthentication no
EOF

# Start sshd
/usr/sbin/sshd -f /tmp/sshd_config_devcontainer &
```

---

## How to Use (For Developers/Users)

### Prerequisites

1. **Server-side configuration** (admin):
	```markup
	# app.ini
	[devcontainer]
	SSH_ENABLED = true
	SSH_PORT = 2222
	SSH_USER = git
	```
2. **Database update** (admin):  
	Update IDE URL templates to include new parameters (see SQL below).
3. **User-side VSCode configuration** (each user):
	**IMPORTANT: Users must manually configure `docker.host` in VSCode settings:**
	Open VSCode Settings (Cmd+, or Ctrl+,), search for `docker.host`, and set:
	```markup
	ssh://root@<server-ip>:<host-ssh-port>
	```
	Or edit `settings.json` directly:
	```json
	{
	  "docker.host": "ssh://root@83.229.127.201:45147"
	}
	```
	**Note:**
	- `<host-ssh-port>` is the **host machine's SSH port** (not container's 2222)
		- User must have SSH access to the host machine
		- User's SSH public key must be in host's `~/.ssh/authorized_keys`

### Usage Flow

1. User opens DevStar web interface
2. User clicks "Open with VSCode" button
3. Browser opens URL: `vscode://mengning.devstar/openProject?...&sshUnified=true&containerName=user-project-xxx...`
4. VSCode devstar extension receives the URL
5. Extension calls `attachToRunningContainer` command with container name
6. Dev Containers extension:
	- Reads `docker.host` from settings
		- Connects to remote Docker daemon via SSH
		- Attaches to the specified container
7. VSCode window opens with container's workspace

### Database SQL Update

```sql
-- Update IDE URL templates to include new parameters
UPDATE system_setting 
SET setting_value = '[
  {"Name":"VSCode","Logo":"/assets/img/ide/vscode.svg","URL":"vscode://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access_token={token}&devstar_username={devstar_username}&devstar_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"},
  {"Name":"Cursor","Logo":"/assets/img/ide/cursor.svg","URL":"cursor://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access_token={token}&devstar_username={devstar_username}&devstar_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"},
  {"Name":"Windsurf","Logo":"/assets/img/ide/windsurf.svg","URL":"windsurf://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access_token={token}&devstar_username={devstar_username}&devstar_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"},
  {"Name":"Trae","Logo":"/assets/img/ide/trae.svg","URL":"trae://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access_token={token}&devstar_username={devstar_username}&devstar_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"}
]'
WHERE setting_key = 'repository.devcontainer.editor-apps';
```

---

## Files Changed

| File | Changes |
| --- | --- |
| `modules/setting/devcontainer.go` | +10 lines: SSH config fields |
| `modules/setting/config.go` | +8 lines: URL template placeholders |
| `services/devcontainer/devcontainer.go` | +56 lines: URL generation logic |
| `routers/web/devcontainer/devcontainer.go` | +20 lines: Parameter parsing |
| `docker/Dockerfile.devstar` | +24 lines: SSH & glibc setup |
| `docker/rootless/usr/local/bin/docker-setup.sh` | +48 lines: SSH server startup |
| `services/devcontainer/workspace_prepare.go` | +102 lines: (reserved for future) |
| `routers/api/devcontainer/devcontainer.go` | +111 lines: (reserved for future) |

---

## Known Limitations

1. **Manual docker.host setup required**: Users must manually configure `docker.host` in VSCode settings
2. **Host SSH access required**: Users need SSH access to the host machine (not just containers)
3. **Global setting**: `docker.host` is a global VSCode setting, may affect other Docker workflows

## Future Improvements

1. Auto-configure `docker.host` in VSCode extension
2. Support per-workspace docker.host settings
3. Consider changing DevStar base image from Alpine to Ubuntu for native Remote-SSH support

---

- Closes [#89](https://devstar.cn/devstar/devstar/issues/89)
- **devstar-vscode (client)**: [devstar/devstar-vscode#8](https://devstar.cn/devstar/devstar-vscode/pulls/8)

\# PR: Unified SSH Entry Point for "Open with VSCode" Feature --- ## Description ### Background & Problem Currently, the "Open with VSCode" feature requires each DevContainer to expose its own SSH port. When a user clicks "Open with VSCode", the system: 1. Gets the container's mapped SSH port (e.g., 32768, 32769, etc.) 2. Generates a URL like \`vscode://mengning.devstar/openProject?port=32768...\` 3. VSCode uses Remote-SSH to connect to that specific port \*\*Problems with this approach:\*\* - Each container needs to run its own SSH server - Dynamic port allocation is complex to manage - Firewall rules become complicated with many ports - Port conflicts can occur \*\*Goal:\*\* Use a single SSH entry point (port 2222) for all containers, eliminating per-container SSH ports. --- ## Solution Exploration Journey We tried 4 different approaches before finding a working solution: ### Approach 1: Remote-SSH to DevStar Main Container \*\*Idea:\*\* SSH into the DevStar main container (port 2222), then use Dev Containers to attach to user containers. \*\*Implementation tried:\*\* \`\`\` vscode://vscode-remote/ssh-remote+devstar-host/workspace/project \`\`\` \*\*Why it failed:\*\* - DevStar main container is based on \*\*Alpine Linux\*\* - VS Code Server requires \*\*glibc\*\*, but Alpine uses \*\*musl libc\*\* - Official Microsoft documentation confirms: "Remote-SSH does NOT support Alpine Linux" - Reference: https://code.visualstudio.com/docs/remote/linux \*\*Error observed:\*\* \`\`\` /root/.vscode-server/bin/.../node: not found \`\`\` --- ### Approach 2: Dynamic devcontainer.json Generation \*\*Idea:\*\* Generate \`devcontainer.json\` pointing to existing container, let Dev Containers extension attach to it. \*\*Implementation tried:\*\* Created files on server: \`\`\`json //.devcontainer/devcontainer.json { "name": "Attach to Container", "dockerComposeFile": "docker-compose.yml", "service": "devcontainer", "workspaceFolder": "/workspace/project" } //.devcontainer/docker-compose.yml services: devcontainer: container\_name: "user-project-container" image: ubuntu:latest \`\`\` \*\*Why it failed:\*\* - Dev Containers extension always tries to \*\*CREATE\*\* new containers via docker-compose - It doesn't attach to existing containers with the same name - Error: \`The container name "/user-project-container" is already in use\` --- ### Approach 3: attached-container URI Scheme \*\*Idea:\*\* Use VSCode's built-in \`attached-container\` URI to directly attach to a container. \*\*Implementation tried:\*\* \`\`\`javascript // Container config const config = { containerName: "user-project-container" }; const hex = Buffer.from(JSON.stringify(config)).toString('hex'); const uri = \`vscode://vscode-remote/attached-container+${hex}/workspace\`; \`\`\` \*\*Variations tested:\*\* 1. Simple containerName only 2. With \`dockerContext\` parameter 3. With \`dockerHost\` in config 4. With \`settings.docker.host\` in config 5. With \`DOCKER\_HOST\` environment variable \*\*Why ALL failed:\*\* - The \`attached-container\` URI scheme \*\*ignores\*\* all docker.host configurations - It always tries to connect to \*\*local\*\* Docker daemon - Error: \`Cannot attach to the container with name/id xxx, it no longer exists\` \*\*Key finding from logs:\*\* \`\`\` // When using command (works): \[13 ms\] Context: devstar-remote ← Uses configured context // When using URI (fails): \[21 ms\] Setting up container: xxx \[25 ms\] Start: Run: docker inspect --type container xxx ← No context, uses local \`\`\` --- ### Approach 4: Docker over SSH + attachToRunningContainer Command \*\*Final working solution!\*\* \*\*Key Discovery:\*\* By reverse-engineering the Dev Containers extension source code, we found: \`\`\`javascript // From extension.js let g = async E => { let b = typeof E == "string"? E: E?.containerDesc?.Id; if (b) { // Direct lookup by name/ID - no picker UI! x = await si(L, b) } else { // Show picker UI x = await hve(t, c.log, L) } } commands.registerCommand("remote-containers.attachToRunningContainer", g) \`\`\` \*\*The command accepts container name as parameter and reads docker.host setting!\*\* \*\*Working flow:\*\* 1. User configures \`docker.host\` in VSCode settings pointing to remote server 2. Extension calls \`vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName)\` 3. Dev Containers extension connects to remote Docker via SSH 4. Attaches directly to specified container --- ## Implementation Details ### Server-Side Changes (This PR) #### 1. New Configuration Options \*\*File: \`modules/setting/devcontainer.go\`\*\* \`\`\`go // Added new config fields type DevContainerConfigType struct { //... existing fields... SSHEnabled bool // Enable unified SSH entry SSHPort int // SSH port (default: 2222) SSHUser string // SSH user (default: git) SSHWorkspacePath string // Workspace path on host } \`\`\` \*\*Configuration in \`app.ini\`:\*\* \`\`\`ini \[devcontainer\] SSH\_ENABLED = true SSH\_PORT = 2222 SSH\_USER = git SSH\_WORKSPACE\_PATH = /var/lib/gitea/devstar-workspace \`\`\` #### 2. URL Template Updates \*\*File: \`modules/setting/config.go\`\*\* Added 3 new placeholders to IDE URL templates: \`\`\`go // Before "vscode://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access\_token={token}&devstar\_username={devstar\_username}&devstar\_domain={domain}" // After "vscode://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access\_token={token}&devstar\_username={devstar\_username}&devstar\_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}" \`\`\` #### 3. URL Generation Logic \*\*File: \`services/devcontainer/devcontainer.go\`\*\* Modified \`Get\_IDE\_TerminalURL()\` function: \`\`\`go func Get\_IDE\_TerminalURL(...) (string, error) { var port, hostname, username string if setting.DevContainerConfig.SSHEnabled { // Unified SSH mode: use configured port port = fmt.Sprintf("%d", setting.DevContainerConfig.SSHPort) hostname = setting.Domain username = setting.DevContainerConfig.SSHUser } else if setting.K8sConfig.Enable { // K8s mode: use NodePort port = fmt.Sprintf("%d", devcontainerApp.Status.NodePortAssigned) hostname = devContainerInfo.DevcontainerHost username = doer.Name } else { // Docker mode: use mapped port mappedPort, \_:= docker\_module.GetMappedPort(ctx, containerName, "22") port = fmt.Sprintf("%d", mappedPort) hostname = devContainerInfo.DevcontainerHost username = doer.Name } url:= "://mengning.devstar/openProject?..." + "&hostname=" + hostname + "&port=" + port + "&username=" + username + "..." // Add unified SSH params if setting.DevContainerConfig.SSHEnabled { url += "&sshUnified=true" url += "&containerName=" + devContainerInfo.Name url += "&workspacePath=" + setting.DevContainerConfig.SSHWorkspacePath } return url, nil } \`\`\` #### 4. Template Parameter Replacement \*\*File: \`routers/web/devcontainer/devcontainer.go\`\*\* Added new fields to \`IDETemplateParams\`: \`\`\`go type IDETemplateParams struct { //... existing fields... SSHUnified string ContainerName string WorkspacePath string } func replaceIDETemplate(template string, params IDETemplateParams) string { //... existing replacements... result = strings.ReplaceAll(result, "{sshUnified}", params.SSHUnified) result = strings.ReplaceAll(result, "{containerName}", params.ContainerName) result = strings.ReplaceAll(result, "{workspacePath}", params.WorkspacePath) return result } \`\`\` #### 5. Docker/SSH Setup \*\*File: \`docker/Dockerfile.devstar\`\*\* \`\`\`dockerfile # Ensure openssh is installed RUN apk --no-cache add openssh openssh-keygen || true # Install glibc (for potential future Alpine Remote-SSH support) RUN apk --no-cache add --virtual.glibc-deps wget ca-certificates && \\ wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \\ wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r1/glibc-2.35-r1.apk && \\ apk add --no-cache --force-overwrite glibc-2.35-r1.apk && \\ rm glibc-2.35-r1.apk && \\ apk del.glibc-deps || echo "glibc installation optional" \`\`\` \*\*File: \`docker/rootless/usr/local/bin/docker-setup.sh\`\*\* \`\`\`bash # DevContainer SSH Setup (port 2222) DEVCONTAINER\_SSH\_PORT=${DEVCONTAINER\_SSH\_PORT:-"2222"} # Setup SSH directory and keys mkdir -p ${HOME}/.ssh && chmod 700 ${HOME}/.ssh ssh-keygen -A 2>/dev/null || true # Create sshd config for port 2222 cat > /tmp/sshd\_config\_devcontainer << EOF Port ${DEVCONTAINER\_SSH\_PORT} ListenAddress 0.0.0.0 PubkeyAuthentication yes PasswordAuthentication no EOF # Start sshd /usr/sbin/sshd -f /tmp/sshd\_config\_devcontainer & \`\`\` --- ## How to Use (For Developers/Users) ### Prerequisites 1. \*\*Server-side configuration\*\* (admin): \`\`\`ini # app.ini \[devcontainer\] SSH\_ENABLED = true SSH\_PORT = 2222 SSH\_USER = git \`\`\` 2. \*\*Database update\*\* (admin): Update IDE URL templates to include new parameters (see SQL below). 3. \*\*User-side VSCode configuration\*\* (each user): \*\*IMPORTANT: Users must manually configure \`docker.host\` in VSCode settings:\*\* Open VSCode Settings (Cmd+, or Ctrl+,), search for \`docker.host\`, and set: \`\`\` ssh://root@<server-ip>:<host-ssh-port> \`\`\` Or edit \`settings.json\` directly: \`\`\`json { "docker.host": "ssh://root@83.229.127.201:45147" } \`\`\` \*\*Note:\*\* - \`<host-ssh-port>\` is the \*\*host machine's SSH port\*\* (not container's 2222) - User must have SSH access to the host machine - User's SSH public key must be in host's \`~/.ssh/authorized\_keys\` ### Usage Flow 1. User opens DevStar web interface 2. User clicks "Open with VSCode" button 3. Browser opens URL: \`vscode://mengning.devstar/openProject?...&sshUnified=true&containerName=user-project-xxx...\` 4. VSCode devstar extension receives the URL 5. Extension calls \`attachToRunningContainer\` command with container name 6. Dev Containers extension: - Reads \`docker.host\` from settings - Connects to remote Docker daemon via SSH - Attaches to the specified container 7. VSCode window opens with container's workspace ### Database SQL Update \`\`\`sql -- Update IDE URL templates to include new parameters UPDATE system\_setting SET setting\_value = '\[ {"Name":"VSCode","Logo":"/assets/img/ide/vscode.svg","URL":"vscode://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access\_token={token}&devstar\_username={devstar\_username}&devstar\_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"}, {"Name":"Cursor","Logo":"/assets/img/ide/cursor.svg","URL":"cursor://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access\_token={token}&devstar\_username={devstar\_username}&devstar\_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"}, {"Name":"Windsurf","Logo":"/assets/img/ide/windsurf.svg","URL":"windsurf://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access\_token={token}&devstar\_username={devstar\_username}&devstar\_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"}, {"Name":"Trae","Logo":"/assets/img/ide/trae.svg","URL":"trae://mengning.devstar/openProject?host={host}&hostname={hostname}&port={port}&username={username}&path={path}&access\_token={token}&devstar\_username={devstar\_username}&devstar\_domain={domain}&sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}"} \]' WHERE setting\_key = 'repository.devcontainer.editor-apps'; \`\`\` --- ## Files Changed | File | Changes | |------|---------| | \`modules/setting/devcontainer.go\` | +10 lines: SSH config fields | | \`modules/setting/config.go\` | +8 lines: URL template placeholders | | \`services/devcontainer/devcontainer.go\` | +56 lines: URL generation logic | | \`routers/web/devcontainer/devcontainer.go\` | +20 lines: Parameter parsing | | \`docker/Dockerfile.devstar\` | +24 lines: SSH & glibc setup | | \`docker/rootless/usr/local/bin/docker-setup.sh\` | +48 lines: SSH server startup | | \`services/devcontainer/workspace\_prepare.go\` | +102 lines: (reserved for future) | | \`routers/api/devcontainer/devcontainer.go\` | +111 lines: (reserved for future) | --- ## Known Limitations 1. \*\*Manual docker.host setup required\*\*: Users must manually configure \`docker.host\` in VSCode settings 2. \*\*Host SSH access required\*\*: Users need SSH access to the host machine (not just containers) 3. \*\*Global setting\*\*: \`docker.host\` is a global VSCode setting, may affect other Docker workflows ## Future Improvements 1. Auto-configure \`docker.host\` in VSCode extension 2. Support per-workspace docker.host settings 3. Consider changing DevStar base image from Alpine to Ubuntu for native Remote-SSH support --- ## Related Issue - Closes https://devstar.cn/devstar/devstar/issues/89 ## Related PR - \*\*devstar-vscode (client)\*\*: https://devstar.cn/devstar/devstar-vscode/pulls/8

于

2个月前

推送 11 个提交

[feat(ssh): add unified SSH entry with devcontainer workspace](https://www.devstar.cn/devstar/devstar/commit/f222489b097db5ef821a5526764d7e24b7e25fdd) [f222489b09](https://www.devstar.cn/devstar/devstar/commit/f222489b097db5ef821a5526764d7e24b7e25fdd)

[feat(ssh): add devcontainer-ssh service on port 2222](https://www.devstar.cn/devstar/devstar/commit/eadac89ff237a7e1493f9a5e74dc5e4b64d81d83) [eadac89ff2](https://www.devstar.cn/devstar/devstar/commit/eadac89ff237a7e1493f9a5e74dc5e4b64d81d83)

[fix: unlock git user and fix authorized\_keys path for SSH on port 2222](https://www.devstar.cn/devstar/devstar/commit/925fdd115030204c0e246a7980ac5fae0e0e4354) [925fdd1150](https://www.devstar.cn/devstar/devstar/commit/925fdd115030204c0e246a7980ac5fae0e0e4354)

```
- Change 'echo git:* | chpasswd -e' to 'passwd -u git' to unlock account
- Add devcontainer-ssh script permissions to Dockerfile
- Fix authorized_keys path to use git user's actual home directory
- Add runtime check to unlock account if still locked in /etc/shadow
```

[fix: add SSH server support to rootless Docker image](https://www.devstar.cn/devstar/devstar/commit/420b290f669fc81548adae3cf66f9f43e85e5308) [420b290f66](https://www.devstar.cn/devstar/devstar/commit/420b290f669fc81548adae3cf66f9f43e85e5308)

```
- Install openssh in Dockerfile.devstar
- Generate SSH host keys at build time with git user permissions
- Unlock git user account for SSH login
- Add sshd startup in docker-setup.sh for port 2222
- Create sshd_config_devcontainer dynamically
```

[chore: remove unused s6 devcontainer-ssh service](https://www.devstar.cn/devstar/devstar/commit/ecdb7cd5ea2a9c679185308a2abd6949953ad85d) [ecdb7cd5ea](https://www.devstar.cn/devstar/devstar/commit/ecdb7cd5ea2a9c679185308a2abd6949953ad85d)

```
The actual build uses docker/Dockerfile.devstar with rootless setup,
not the main Dockerfile with s6 services.
```

[fix: change default SSH\_WORKSPACE\_PATH to /var/lib/gitea/devstar-workspace](https://www.devstar.cn/devstar/devstar/commit/0597d7aa9702bd822cde0568bb92188c1f9fcfa2) [0597d7aa97](https://www.devstar.cn/devstar/devstar/commit/0597d7aa9702bd822cde0568bb92188c1f9fcfa2)

```
The rootless container uses /var/lib/gitea as data directory,
not /data which doesn't exist in the rootless setup.
```

[fix: add sshUnified, containerName, workspacePath to IDE URL templates](https://www.devstar.cn/devstar/devstar/commit/34b8b8cba2dfa7810fab3313e74e33bed906a440) [34b8b8cba2](https://www.devstar.cn/devstar/devstar/commit/34b8b8cba2dfa7810fab3313e74e33bed906a440)

```
- Add new fields to IDETemplateParams struct
- Update replaceIDETemplate to handle new placeholders
- Add new parameters to IDETemplateParams initialization in GetDevContainerDetails
- Update DefaultDevContainerEditorApps URL templates with new parameters
```

[debug: add logging for SSHEnabled config check](https://www.devstar.cn/devstar/devstar/commit/91ec38f866909c72654a85b3a73c866ffdc352cf) [91ec38f866](https://www.devstar.cn/devstar/devstar/commit/91ec38f866909c72654a85b3a73c866ffdc352cf)

[debug: add logging for final URL generation](https://www.devstar.cn/devstar/devstar/commit/00cca9d680ee876c2e7208fb346ee0d177a0c995) [00cca9d680](https://www.devstar.cn/devstar/devstar/commit/00cca9d680ee876c2e7208fb346ee0d177a0c995)

[debug: add logging for IDE URL template replacement](https://www.devstar.cn/devstar/devstar/commit/0d79007916519c8a257e931957d91291405820ff) [0d79007916](https://www.devstar.cn/devstar/devstar/commit/0d79007916519c8a257e931957d91291405820ff)

[feat(docker): add glibc for VS Code Server compatibility on Alpine](https://www.devstar.cn/devstar/devstar/commit/93d9b475831a69c95986856bb76ad1ecf5478a18) [93d9b47583](https://www.devstar.cn/devstar/devstar/commit/93d9b475831a69c95986856bb76ad1ecf5478a18)

于[

2个月前

](https://www.devstar.cn/devstar/devstar/pulls/108#event-1397)[引用合并请求 来自 devstar/devstar-vscode](https://www.devstar.cn/devstar/devstar-vscode/pulls/8)

[**feat: Implement Docker over SSH attachment for unified SSH entry point** #8](https://www.devstar.cn/devstar/devstar-vscode/pulls/8)

### 测试状态 ❌ 失败 (Failed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ❌ 失败 (Failed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

welldone! 比我原来预想的还要更简洁一点。不过有以下几个问题要注意：

- 这种方式用户权限过大，得限制用户仅能访问指定的容器和指定workspace目录；
- is the host machine's SSH port (not container's 2222) 这地方理解有误，2222就可以理解为host machine's SSH port，因为我们是在Alpine Linux容器环境中部署的，容器应该理解为用户的Dev Container容器；
- 尽可能对devstar-vscode客户端屏蔽掉系统内部的配置信息，精简配置项，逻辑上仅需要包括Host、Port（默认2222）、user name、repo name、临时会话认证信息，逻辑上的执行步骤：

1、用临时会话信息认证可以将SSH公钥上传；  
2、自动配置 "docker.host": "ssh://user name@Host:2222"  
3、vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName); 其中containerName按约定规则由user name和repo name生成。  
4、登录成功后进入/workspace/repo name/ 目录

welldone! 比我原来预想的还要更简洁一点。不过有以下几个问题要注意： - 这种方式用户权限过大，得限制用户仅能访问指定的容器和指定workspace目录； - <host-ssh-port> is the host machine's SSH port (not container's 2222) 这地方理解有误，2222就可以理解为host machine's SSH port，因为我们是在Alpine Linux容器环境中部署的，容器应该理解为用户的Dev Container容器； - 尽可能对devstar-vscode客户端屏蔽掉系统内部的配置信息，精简配置项，逻辑上仅需要包括Host、Port（默认2222）、user name、repo name、临时会话认证信息，逻辑上的执行步骤： 1、用临时会话信息认证可以将SSH公钥上传； 2、自动配置 "docker.host": "ssh://user name@Host:2222" 3、vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName); 其中containerName按约定规则由user name和repo name生成。 4、登录成功后进入/workspace/repo name/ 目录

于

上个月

推送 2 个提交

[feat(container): simplify container name to {username}-{reponame}](https://www.devstar.cn/devstar/devstar/commit/9173290374d255345f3bd0a0ad2217ba957e3e5b) [9173290374](https://www.devstar.cn/devstar/devstar/commit/9173290374d255345f3bd0a0ad2217ba957e3e5b)

```
Remove UUID suffix from container name. New format: {username}-{reponame}
This allows client to generate the same container name without server passing it.
```

[feat(container): add devcontainer labels for VSCode display name](https://www.devstar.cn/devstar/devstar/commit/6223f60ad7f66494c7c13bcfdec150bca7673998) [6223f60ad7](https://www.devstar.cn/devstar/devstar/commit/6223f60ad7f66494c7c13bcfdec150bca7673998)

```
- Add labels parameter to CreateAndStartContainer function
- Set devcontainer.local_folder label to /workspace/{reponame}
- Set devcontainer.config_file label for devcontainer.json path
- Remove unused uuid import from devcontainer_utils.go

These labels enable VSCode Dev Containers extension to show a friendly
container name in the bottom-left corner (e.g., 'dev-reponame')
```

于

上个月

推送 1 个提交

[fix(container): add devcontainer labels to docker create command](https://www.devstar.cn/devstar/devstar/commit/0e71d9f312361f733f8596cb3f1d5195f2f39642) [0e71d9f312](https://www.devstar.cn/devstar/devstar/commit/0e71d9f312361f733f8596cb3f1d5195f2f39642)

```
The CreateDevContainerByDockerCommand function uses docker CLI instead
of Docker API. Add --label flags to include devcontainer.local_folder
and devcontainer.config_file for VSCode Dev Containers display name.
```

于

上个月

推送 1 个提交

[feat(container): add devcontainer.metadata label for workspace config](https://www.devstar.cn/devstar/devstar/commit/7c9a246475df16ebcdf5ae6aea04041c6916aee2) [7c9a246475](https://www.devstar.cn/devstar/devstar/commit/7c9a246475df16ebcdf5ae6aea04041c6916aee2)

```
Add metadata label containing workspaceFolder configuration.
This helps Dev Containers extension identify the correct working directory.
```

## New Commits

- `feat(container): simplify container name to {username}-{reponame}` ([`9173290374`](https://www.devstar.cn/devstar/devstar/commit/9173290374))
- `feat(container): add devcontainer labels for VSCode display name` ([`6223f60ad7`](https://www.devstar.cn/devstar/devstar/commit/6223f60ad7))
- `fix(container): add devcontainer labels to docker create command` ([`0e71d9f312`](https://www.devstar.cn/devstar/devstar/commit/0e71d9f312))
- `feat(container): add devcontainer.metadata label for workspace config` ([`7c9a246475`](https://www.devstar.cn/devstar/devstar/commit/7c9a246475))

## Changes

### 1\. Simplify Container Name

Changed container naming format from `{username}-{reponame}-{uuid}` to `{username}-{reponame}`.

**Naming Rules:**

- Remove non-alphanumeric characters
- Convert to lowercase
- Truncate username to 15 chars, reponame to 31 chars

**Before:** `shizi-base123123-a0df5266ef9011f`  
**After:** `shizi-base123123`

**File:** `services/devcontainer/devcontainer_utils.go`

Added `--label` flags to `docker create` command:

```bash
--label "devcontainer.local_folder=/workspace/{reponame}"
--label "devcontainer.config_file=/workspace/{reponame}/.devcontainer/devcontainer.json"
--label 'devcontainer.metadata=[{"remoteUser":"root","workspaceFolder":"/workspace/{reponame}"}]'
```

These labels help VSCode Dev Containers extension:

- Determine the workspace folder to open
- Provide configuration metadata

**Files:**

- `services/devcontainer/docker_agent.go`
- `modules/docker/docker_api.go`
- `services/runners/runners.go`

## Known Limitation

The container display name in VSCode shows `Container ubuntu:latest ({container-name})`. This format is hardcoded in the Dev Containers extension. See discussion file for proposed solutions.

\# Update: Container Naming and Labels for VSCode Integration ## New Commits - \`feat(container): simplify container name to {username}-{reponame}\` (9173290374) - \`feat(container): add devcontainer labels for VSCode display name\` (6223f60ad7) - \`fix(container): add devcontainer labels to docker create command\` (0e71d9f312) - \`feat(container): add devcontainer.metadata label for workspace config\` (7c9a246475) ## Changes ### 1. Simplify Container Name Changed container naming format from \`{username}-{reponame}-{uuid}\` to \`{username}-{reponame}\`. \*\*Naming Rules:\*\* - Remove non-alphanumeric characters - Convert to lowercase - Truncate username to 15 chars, reponame to 31 chars \*\*Before:\*\* \`shizi-base123123-a0df5266ef9011f\` \*\*After:\*\* \`shizi-base123123\` \*\*File:\*\* \`services/devcontainer/devcontainer\_utils.go\` ### 2. Add Devcontainer Labels Added \`--label\` flags to \`docker create\` command: \`\`\`bash --label "devcontainer.local\_folder=/workspace/{reponame}" --label "devcontainer.config\_file=/workspace/{reponame}/.devcontainer/devcontainer.json" --label 'devcontainer.metadata=\[{"remoteUser":"root","workspaceFolder":"/workspace/{reponame}"}\]' \`\`\` These labels help VSCode Dev Containers extension: - Determine the workspace folder to open - Provide configuration metadata \*\*Files:\*\* - \`services/devcontainer/docker\_agent.go\` - \`modules/docker/docker\_api.go\` - \`services/runners/runners.go\` ## Known Limitation The container display name in VSCode shows \`Container ubuntu:latest ({container-name})\`. This format is hardcoded in the Dev Containers extension. See discussion file for proposed solutions.

> welldone! 比我原来预想的还要更简洁一点。不过有以下几个问题要注意：
> 
> - 这种方式用户权限过大，得限制用户仅能访问指定的容器和指定workspace目录；
> - is the host machine's SSH port (not container's 2222) 这地方理解有误，2222就可以理解为host machine's SSH port，因为我们是在Alpine Linux容器环境中部署的，容器应该理解为用户的Dev Container容器；
> - 尽可能对devstar-vscode客户端屏蔽掉系统内部的配置信息，精简配置项，逻辑上仅需要包括Host、Port（默认2222）、user name、repo name、临时会话认证信息，逻辑上的执行步骤：
> 
> 1、用临时会话信息认证可以将SSH公钥上传；  
> 2、自动配置 "docker.host": "ssh://user name@Host:2222"  
> 3、vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName); 其中containerName按约定规则由user name和repo name生成。  
> 4、登录成功后进入/workspace/repo name/ 目录

Here's the current status:

## Completed

### 1\. Temporary session authentication for SSH public key upload

Done. The extension automatically:

- Checks if user has SSH keys, creates if not
- Uploads public key to server via DevStar API

### 2\. Auto-configure docker.host

Done. The extension writes to VSCode settings.json:

```json
"docker.host": "ssh://{username}@{Host}:2222"
```

### 3\. attachToRunningContainer with containerName

Done. Container name is generated by convention:

```markup
containerName = {username}-{reponame}
```

Rules: remove non-alphanumeric chars, lowercase, truncate (username: 15 chars, reponame: 31 chars)

### 4\. Open /workspace/{reponame} directory after login

Done. The extension sets imageConfig before attaching, so VSCode opens the correct workspace folder.

## Remaining Issue: Container Display Name

Currently shows: `Container ubuntu:latest (shizi-base123123)`

### Root Cause

The display format `Container {image} ({container-name})` is **hardcoded** in the Dev Containers extension source code:

```javascript
"Container {0} ({1}){2}"
```

Where:

- `{0}` = Image name (e.g., `ubuntu:latest`)
- `{1}` = Container name (e.g., `shizi-base123123`)
- `{2}` = Additional info

This format is used for "Attached Container" mode. When VSCode recognizes a container as a proper "Dev Container" (created via devcontainer.json), it displays `Dev Container: {name}` instead.

### Proposed Solutions

**Option 1: Modify Image Tag**

```bash
docker tag ubuntu:latest dev-base123123:latest
docker create --name shizi-base123123 dev-base123123:latest ...
```

Result: `Container dev-base123123:latest (shizi-base123123)`

- Pros: Image name becomes meaningful
- Cons: Creates many image tags, requires cleanup

**Option 2: Modify Container Name**  
Change from `{username}-{reponame}` to `dev-{reponame}`  
Result: `Container ubuntu:latest (dev-base123123)`

- Pros: Simple change
- Cons: Loses username (potential naming conflicts)

**Option 3: Use Named Container Configuration** - Not Viable  
Create a named container configuration file in VSCode's globalStorage.

- Result: Investigated, but the configuration file doesn't support display name customization. Only supports `workspaceFolder`, `extensions`, `settings`, etc.

**Option 4: Make Container Appear as "Real" Dev Container** - Not Viable  
Use `remote-containers.reopenInContainer` or similar command instead of `attachToRunningContainer`.

- Result: These commands create new containers rather than attach to existing ones, and may not work with remote Docker via SSH.

**Option 5: Accept Current Behavior**  
Keep current implementation.  
Result: `Container ubuntu:latest (shizi-base123123)`

- Pros: No additional changes, stable
- Cons: Display name not as user-friendly

What's the preferred approach?

> 用户权限过大，得限制用户仅能访问指定的容器和指定workspace目录

Currently, users connect via Docker over SSH and can theoretically access other containers. To restrict this, we could:

1. **Container-level**: Use Docker authorization plugins to limit container access per user
2. **SSH-level**: Configure SSH to only allow specific Docker commands
3. **Network-level**: Use Docker networks to isolate containers

\> welldone! 比我原来预想的还要更简洁一点。不过有以下几个问题要注意： > > - 这种方式用户权限过大，得限制用户仅能访问指定的容器和指定workspace目录； > - <host-ssh-port> is the host machine's SSH port (not container's 2222) 这地方理解有误，2222就可以理解为host machine's SSH port，因为我们是在Alpine Linux容器环境中部署的，容器应该理解为用户的Dev Container容器； > - 尽可能对devstar-vscode客户端屏蔽掉系统内部的配置信息，精简配置项，逻辑上仅需要包括Host、Port（默认2222）、user name、repo name、临时会话认证信息，逻辑上的执行步骤： > > 1、用临时会话信息认证可以将SSH公钥上传； > 2、自动配置 "docker.host": "ssh://user name@Host:2222" > 3、vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName); 其中containerName按约定规则由user name和repo name生成。 > 4、登录成功后进入/workspace/repo name/ 目录 Here's the current status: ## Completed ### 1. Temporary session authentication for SSH public key upload Done. The extension automatically: - Checks if user has SSH keys, creates if not - Uploads public key to server via DevStar API ### 2. Auto-configure docker.host Done. The extension writes to VSCode settings.json: \`\`\`json "docker.host": "ssh://{username}@{Host}:2222" \`\`\` ### 3. attachToRunningContainer with containerName Done. Container name is generated by convention: \`\`\` containerName = {username}-{reponame} \`\`\` Rules: remove non-alphanumeric chars, lowercase, truncate (username: 15 chars, reponame: 31 chars) ### 4. Open /workspace/{reponame} directory after login Done. The extension sets imageConfig before attaching, so VSCode opens the correct workspace folder. ## Remaining Issue: Container Display Name Currently shows: \`Container ubuntu:latest (shizi-base123123)\` ### Root Cause The display format \`Container {image} ({container-name})\` is \*\*hardcoded\*\* in the Dev Containers extension source code: \`\`\`javascript "Container {0} ({1}){2}" \`\`\` Where: - \`{0}\` = Image name (e.g., \`ubuntu:latest\`) - \`{1}\` = Container name (e.g., \`shizi-base123123\`) - \`{2}\` = Additional info This format is used for "Attached Container" mode. When VSCode recognizes a container as a proper "Dev Container" (created via devcontainer.json), it displays \`Dev Container: {name}\` instead. ### Proposed Solutions \*\*Option 1: Modify Image Tag\*\* \`\`\`bash docker tag ubuntu:latest dev-base123123:latest docker create --name shizi-base123123 dev-base123123:latest... \`\`\` Result: \`Container dev-base123123:latest (shizi-base123123)\` - Pros: Image name becomes meaningful - Cons: Creates many image tags, requires cleanup \*\*Option 2: Modify Container Name\*\* Change from \`{username}-{reponame}\` to \`dev-{reponame}\` Result: \`Container ubuntu:latest (dev-base123123)\` - Pros: Simple change - Cons: Loses username (potential naming conflicts) \*\*Option 3: Use Named Container Configuration\*\* - Not Viable Create a named container configuration file in VSCode's globalStorage. - Result: Investigated, but the configuration file doesn't support display name customization. Only supports \`workspaceFolder\`, \`extensions\`, \`settings\`, etc. \*\*Option 4: Make Container Appear as "Real" Dev Container\*\* - Not Viable Use \`remote-containers.reopenInContainer\` or similar command instead of \`attachToRunningContainer\`. - Result: These commands create new containers rather than attach to existing ones, and may not work with remote Docker via SSH. \*\*Option 5: Accept Current Behavior\*\* Keep current implementation. Result: \`Container ubuntu:latest (shizi-base123123)\` - Pros: No additional changes, stable - Cons: Display name not as user-friendly What's the preferred approach? ## About User Permission Restriction > 用户权限过大，得限制用户仅能访问指定的容器和指定workspace目录 Currently, users connect via Docker over SSH and can theoretically access other containers. To restrict this, we could: 1. \*\*Container-level\*\*: Use Docker authorization plugins to limit container access per user 2. \*\*SSH-level\*\*: Configure SSH to only allow specific Docker commands 3. \*\*Network-level\*\*: Use Docker networks to isolate containers

于

上个月

评审

<table><colgroup><col width="50"> <col width="50"> <col width="10"> <col width="10"> <col></colgroup><tbody><tr><td colspan="2"></td><td></td><td></td><td><code>@@ -0,0 +1,102 @@</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>// Copyright 2024 The Gitea Authors. All rights reserved.</code></td></tr></tbody></table>

于

上个月

推送 1 个提交

[Merge branch 'main' into feat/ssh-refactor](https://www.devstar.cn/devstar/devstar/commit/183efa3dfaca08baa778cb6a4b601b2425d5896f) [183efa3dfa](https://www.devstar.cn/devstar/devstar/commit/183efa3dfaca08baa778cb6a4b601b2425d5896f)

### 测试状态 ❌ 失败 (Failed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ❌ 失败 (Failed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于[

上个月

](https://www.devstar.cn/devstar/devstar/pulls/108#event-1486)在代码提交中引用该工单

[feat: Implement Docker over SSH attachment for unified SSH entry point (#8)](https://www.devstar.cn/devstar/devstar-vscode/commit/49ed02ee462269937bbdbbc09ae82136a655f54e)

于

上个月

推送 1 个提交

于

上个月

推送 1 个提交

[fix(install): prepare data volume permissions before starting container](https://www.devstar.cn/devstar/devstar/commit/51bf2b0b520dfb452dd000dca05d5b8fcfe8e5a5) [51bf2b0b52](https://www.devstar.cn/devstar/devstar/commit/51bf2b0b520dfb452dd000dca05d5b8fcfe8e5a5)

```
When using bind mount (path contains /), pre-create directories and
set correct ownership (UID 1000 = git user in container) before
starting the container. This fixes 'chmod: Operation not permitted'
errors on first run.
```

### 测试状态 ❌ 失败 (Failed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ❌ 失败 (Failed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

### 测试状态 ❌ 失败 (Failed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ❌ 失败 (Failed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于

上个月

推送 1 个提交

[fix(install): fix named volume permissions by using docker exec -u root](https://www.devstar.cn/devstar/devstar/commit/78bca576f448bf9386bc7e464fb933466b4c7784) [78bca576f4](https://www.devstar.cn/devstar/devstar/commit/78bca576f448bf9386bc7e464fb933466b4c7784)

```
Docker named volumes are initially owned by root. After starting the
container, use 'docker exec -u root' to chown directories to git user
(UID=1000), then restart the container.

This fixes the 'chmod: Operation not permitted' error on first run
for both named volumes and bind mounts.
```

于

上个月

推送 1 个提交

[fix(docker): fix /var/lib/gitea/git ownership in Dockerfile](https://www.devstar.cn/devstar/devstar/commit/1d7daba3b59a7940621f1c322c6d6c4e83a145fb) [1d7daba3b5](https://www.devstar.cn/devstar/devstar/commit/1d7daba3b59a7940621f1c322c6d6c4e83a145fb)

```
The root cause of 'chmod: Operation not permitted' error was that
/var/lib/gitea/git directory was owned by root, not git user.

Previously only .ssh subdirectory was chowned:
  chown -R git:git /var/lib/gitea/git/.ssh

Now the entire git directory is chowned:
  chown -R git:git /var/lib/gitea/git

Also reverts the workaround code in install.sh that was added in
commits 51bf2b0 and 78bca57, as they are no longer needed.
```

### 测试状态 ❌ 失败 (Failed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ❌ 失败 (Failed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

### 测试状态 ❌ 失败 (Failed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ❌ 失败 (Failed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于

上个月

推送 1 个提交

[feat(ssh): integrate docker commands into Gitea SSH for DevContainer access](https://www.devstar.cn/devstar/devstar/commit/59cb856d3fa60898c9bc51e286db5bc9978591b5) [59cb856d3f](https://www.devstar.cn/devstar/devstar/commit/59cb856d3fa60898c9bc51e286db5bc9978591b5)

```
Enable VSCode Dev Containers to connect via Gitea's built-in SSH (port 2222)
instead of requiring a separate sshd service.

Changes:
- cmd/serv.go: Add runDockerCommand() to handle docker commands via SSH
  - Whitelist allowed commands: ps, inspect, exec, start, stop, attach, logs
  - Security: users can only operate their own containers (name prefix check)
- docker-setup.sh: Remove standalone sshd startup (no longer needed)

This allows users to use a single SSH key for both git operations and
DevContainer access. VSCode's 'Docker over SSH' now works through Gitea SSH.

Flow: ssh git@host 'docker ps' → Gitea SSH → serv → runDockerCommand()
```

### 测试状态 ✅ 通过 (Passed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ✅ 通过 (Passed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于

上个月

推送 1 个提交

[Merge remote-tracking branch 'origin/main' into feat/ssh-refactor](https://www.devstar.cn/devstar/devstar/commit/d790c4bb5677c34cf2d7cb66cefbb283ca220fe8) [d790c4bb56](https://www.devstar.cn/devstar/devstar/commit/d790c4bb5677c34cf2d7cb66cefbb283ca220fe8)

### 测试状态 ✅ 通过 (Passed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ✅ 通过 (Passed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于

上个月

推送 1 个提交

[fix(ssh): add 'system' to allowed docker subcommands for dial-stdio](https://www.devstar.cn/devstar/devstar/commit/22405464a6b67f24b55defd82fa59c15bf6472b5) [22405464a6](https://www.devstar.cn/devstar/devstar/commit/22405464a6b67f24b55defd82fa59c15bf6472b5)

```
Docker over SSH requires 'docker system dial-stdio' to establish API connection.
Without this, VSCode Dev Containers cannot connect via Docker over SSH.
```

### 测试状态 ✅ 通过 (Passed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ✅ 通过 (Passed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于

上个月

评审

<table><colgroup><col width="50"> <col width="50"> <col width="10"> <col width="10"> <col></colgroup><tbody><tr><td colspan="2"></td><td></td><td></td><td><code>@@ -240,2 +240,4 @@</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>  echo "容器名称 '$CONTAINER_NAME' 已保存到配置文件"</code></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td><code>  sudo docker run --restart=always --name $CONTAINER_NAME -d  -p $PORT:3000 -p $SSH_PORT:$SSH_PORT -v /var/run/docker.sock:/var/run/docker.sock -v ${DATA_VOLUME}:/var/lib/gitea -v ${DATA_VOLUME}:/etc/gitea $IMAGE_STR</code></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>

- 不是以项目的方式进入的，没有进入项目目录
[![9f176ffeadcea380426f042fea79b947.png](https://www.devstar.cn/devstar/devstar/attachments/edc58f00-0d1e-403a-956d-f53217061679)](https://www.devstar.cn/devstar/devstar/attachments/edc58f00-0d1e-403a-956d-f53217061679)

\- 不是以项目的方式进入的，没有进入项目目录 <img width="637" alt="9f176ffeadcea380426f042fea79b947.png" src="attachments/edc58f00-0d1e-403a-956d-f53217061679">

[**9f176ffeadcea380426f042fea79b947.png**](https://devstar.cn/attachments/edc58f00-0d1e-403a-956d-f53217061679 "在新的标签页中查看「9f176ffeadcea380426f042fea79b947.png」")

71 KiB

于

上个月

评审

<table><colgroup><col width="50"> <col width="50"> <col width="10"> <col width="10"> <col></colgroup><tbody><tr><td colspan="2"></td><td></td><td></td><td><code>@@ -225,0 +276,4 @@</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	Where("user_id = ? AND repo_id = ?", ctx.Doer.ID, repoId).</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	Get(&devContainerInfo)</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>if err != nil || !has {</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>failedResult := Result.ResultType{</code></td></tr></tbody></table>

于

上个月

评审

<table><colgroup><col width="50"> <col width="50"> <col width="10"> <col width="10"> <col></colgroup><tbody><tr><td colspan="2"></td><td></td><td></td><td><code>@@ -90,0 +91,4 @@</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	// devcontainer.local_folder 会被用于显示名称</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	devcontainerLabels := map[string]string{</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>		"devcontainer.local_folder": fmt.Sprintf("/workspace/%s", repo.Name),</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>		"devcontainer.config_file":  fmt.Sprintf("/workspace/%s/.devcontainer/devcontainer.json", repo.Name),</code></td></tr></tbody></table>

于

上个月

评审

<table><colgroup><col width="50"> <col width="50"> <col width="10"> <col width="10"> <col></colgroup><tbody><tr><td colspan="2"></td><td></td><td></td><td><code>@@ -0,0 +16,4 @@</code></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td><code>// WorkspaceConfig 包含准备 workspace 所需的配置</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>type WorkspaceConfig struct {</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>ContainerName   string // 容器名称</code></td></tr></tbody></table>

于

上个月

评审

<table><colgroup><col width="50"> <col width="50"> <col width="10"> <col width="10"> <col></colgroup><tbody><tr><td colspan="2"></td><td></td><td></td><td><code>@@ -299,1 +306,4 @@</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	startCommand += " " + strings.Join(configurationModel.RunArgs, " ") + " "</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	// 添加 devcontainer labels，用于 VSCode Dev Containers 显示友好的容器名和工作目录</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	startCommand += fmt.Sprintf(` --label "devcontainer.local_folder=/workspace/%s" `, repo.Name)</code></td></tr><tr><td></td><td></td><td></td><td></td><td><code>	startCommand += fmt.Sprintf(` --label "devcontainer.config_file=/workspace/%s/.devcontainer/devcontainer.json" `, repo.Name)</code></td></tr></tbody></table>

于

上个月

推送 7 个提交

### 59cb856 feat(ssh): integrate docker commands into Gitea SSH

Previously, DevStar required two separate SSH services: Gitea's built-in SSH (port 2222) for git operations and a standalone sshd for DevContainer access. This commit consolidates them by integrating Docker command execution directly into Gitea's SSH server.

**Implementation:** Added `runDockerCommand()` function in `cmd/serv.go` (lines 102-180). When SSH command starts with `docker`, it routes to this handler instead of normal git command processing. The function validates user identity via SSH key, then executes the docker command with stdin/stdout/stderr passthrough.

**Security model:** Whitelist-based command filtering allows only `ps`, `inspect`, `exec`, `start`, `stop`, `attach`, `logs`, `version`, `info`, and `system`. For sensitive commands (`exec`, `start`, `stop`, `attach`, `logs`), container ownership is validated - users can only operate containers prefixed with their sanitized username. The `sanitizeUsername()` function (lines 182-195) converts username to lowercase alphanumeric, max 15 chars.

```markup
sanitizedUsername := sanitizeUsername(user.Name)  // "John.Doe" -> "johndoe"
if !strings.HasPrefix(strings.ToLower(containerName), sanitizedUsername+"-") {
    return fail(ctx, "Access denied", "You can only access your own containers")
}
```

**Data flow:** `ssh git@devstar.cn:2222 'docker ps'` → Gitea SSH → `serv.go` → `runDockerCommand()` → `exec.Command("docker", args...)` → Docker daemon

### 22405464a6 fix(ssh): add 'system' to allowed docker subcommands

VSCode Dev Containers uses `docker system dial-stdio` to establish Docker API connection over SSH. This creates a bidirectional pipe to the remote Docker daemon's socket, enabling all subsequent Docker API calls to be tunneled through SSH. Without this subcommand in the whitelist, connection fails with exit status 255.

---

### 1d7daba fix(docker): fix /var/lib/gitea/git ownership in Dockerfile

Root cause of `chmod: Operation not permitted` error: `/var/lib/gitea/git` was owned by root. The Dockerfile previously only chowned the `.ssh` subdirectory:

```dockerfile
# Before:
RUN chown -R git:git /var/lib/gitea/git/.ssh
# After:
RUN chown -R git:git /var/lib/gitea/git
```

Commits `51bf2b0` and `78bca57` were intermediate workarounds that have been reverted.

---

## PR Review Fixes

### 42070d5 Copyright header

Updated `workspace_prepare.go` copyright to "Mengning Software".

### 2e93c98 Revert install.sh

Reverted unnecessary modifications after Dockerfile fix.

### f65403c, 8daa3c8 Code indentation

Fixed tab/space inconsistency in `devcontainer.go` and `workspace_prepare.go`.

### 37efd89 Default config path

Changed default from `.devcontainer/devcontainer.json` to `.devstar/devcontainer.json`.

### 44263720c1 Parameterize workspace paths

Introduced configurable settings in `modules/setting/devcontainer.go`:

```markup
UserWorkspaceBasePath   = "/var/lib/gitea/user-workspace"  // Host path for user workspaces
ContainerWorkspaceDir   = "/workspace"                      // Mount point inside container
DevcontainerConfigPath  = ".devstar/devcontainer.json"      // Relative config path
```

All hardcoded paths in `docker_agent.go` and `devcontainer.go` now reference these config values, configurable via `app.ini` under `[devcontainer]` section.

### d4ef916 User-level workspace volume mount

Each user's workspace is mounted from a separate host directory for isolation:

```markup
// docker_agent.go lines 305-310
if userWorkspaceBasePath != "" {
    startCommand += fmt.Sprintf(\` -v %s/%s:%s \`, userWorkspaceBasePath, currentUser.Name, containerWorkspaceDir)
}
// Result: -v /var/lib/gitea/user-workspace/alice:/workspace
```

\### \`59cb856\` feat(ssh): integrate docker commands into Gitea SSH Previously, DevStar required two separate SSH services: Gitea's built-in SSH (port 2222) for git operations and a standalone sshd for DevContainer access. This commit consolidates them by integrating Docker command execution directly into Gitea's SSH server. \*\*Implementation:\*\* Added \`runDockerCommand()\` function in \`cmd/serv.go\` (lines 102-180). When SSH command starts with \`docker\`, it routes to this handler instead of normal git command processing. The function validates user identity via SSH key, then executes the docker command with stdin/stdout/stderr passthrough. \*\*Security model:\*\* Whitelist-based command filtering allows only \`ps\`, \`inspect\`, \`exec\`, \`start\`, \`stop\`, \`attach\`, \`logs\`, \`version\`, \`info\`, and \`system\`. For sensitive commands (\`exec\`, \`start\`, \`stop\`, \`attach\`, \`logs\`), container ownership is validated - users can only operate containers prefixed with their sanitized username. The \`sanitizeUsername()\` function (lines 182-195) converts username to lowercase alphanumeric, max 15 chars. \`\`\`go sanitizedUsername:= sanitizeUsername(user.Name) // "John.Doe" -> "johndoe" if!strings.HasPrefix(strings.ToLower(containerName), sanitizedUsername+"-") { return fail(ctx, "Access denied", "You can only access your own containers") } \`\`\` \*\*Data flow:\*\* \`ssh git@devstar.cn:2222 'docker ps'\` → Gitea SSH → \`serv.go\` → \`runDockerCommand()\` → \`exec.Command("docker", args...)\` → Docker daemon ### \`22405464a6\` fix(ssh): add 'system' to allowed docker subcommands VSCode Dev Containers uses \`docker system dial-stdio\` to establish Docker API connection over SSH. This creates a bidirectional pipe to the remote Docker daemon's socket, enabling all subsequent Docker API calls to be tunneled through SSH. Without this subcommand in the whitelist, connection fails with exit status 255. --- ## Volume Permission Fixes ### \`1d7daba\` fix(docker): fix /var/lib/gitea/git ownership in Dockerfile Root cause of \`chmod: Operation not permitted\` error: \`/var/lib/gitea/git\` was owned by root. The Dockerfile previously only chowned the \`.ssh\` subdirectory: \`\`\`dockerfile # Before: RUN chown -R git:git /var/lib/gitea/git/.ssh # After: RUN chown -R git:git /var/lib/gitea/git \`\`\` Commits \`51bf2b0\` and \`78bca57\` were intermediate workarounds that have been reverted. --- ## PR Review Fixes ### \`42070d5\` Copyright header Updated \`workspace\_prepare.go\` copyright to "Mengning Software". ### \`2e93c98\` Revert install.sh Reverted unnecessary modifications after Dockerfile fix. ### \`f65403c\`, \`8daa3c8\` Code indentation Fixed tab/space inconsistency in \`devcontainer.go\` and \`workspace\_prepare.go\`. ### \`37efd89\` Default config path Changed default from \`.devcontainer/devcontainer.json\` to \`.devstar/devcontainer.json\`. ### \`44263720c1\` Parameterize workspace paths Introduced configurable settings in \`modules/setting/devcontainer.go\`: \`\`\`go UserWorkspaceBasePath = "/var/lib/gitea/user-workspace" // Host path for user workspaces ContainerWorkspaceDir = "/workspace" // Mount point inside container DevcontainerConfigPath = ".devstar/devcontainer.json" // Relative config path \`\`\` All hardcoded paths in \`docker\_agent.go\` and \`devcontainer.go\` now reference these config values, configurable via \`app.ini\` under \`\[devcontainer\]\` section. ### \`d4ef916\` User-level workspace volume mount Each user's workspace is mounted from a separate host directory for isolation: \`\`\`go // docker\_agent.go lines 305-310 if userWorkspaceBasePath!= "" { startCommand += fmt.Sprintf(\` -v %s/%s:%s \`, userWorkspaceBasePath, currentUser.Name, containerWorkspaceDir) } // Result: -v /var/lib/gitea/user-workspace/alice:/workspace \`\`\`

> - 不是以项目的方式进入的，没有进入项目目录
> [![9f176ffeadcea380426f042fea79b947.png](https://www.devstar.cn/devstar/devstar/attachments/edc58f00-0d1e-403a-956d-f53217061679)](https://www.devstar.cn/devstar/devstar/attachments/edc58f00-0d1e-403a-956d-f53217061679)

## Auto-Open Workspace Folder

### Problem

"Attach to Running Container" opens root directory (`/`) instead of project workspace (`/workspace/reponame`).

### Server-side (docker\_agent.go lines 315-321)

Three Docker labels are set on container creation. The `devcontainer.metadata` label is key - Dev Containers extension reads `workspaceFolder` from it:

```markup
devcontainerMetadata := fmt.Sprintf(\`[{"remoteUser":"root","workspaceFolder":"%s/%s"}]\`, containerWorkspaceDir, repo.Name)
startCommand += fmt.Sprintf(\` --label 'devcontainer.metadata=%s' \`, devcontainerMetadata)
```

### Client-side (devstar-vscode extension)

Dev Containers extension reads per-container settings from `nameConfigs` directory. Our extension creates config file before `attachToRunningContainer`:

```typescript
// src/remote-container.ts lines 205-213
const workspaceFolder = \`/workspace/${repoName}\`;
await this.setContainerNameConfig(containerName, workspaceFolder);  // Write config first
await vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName);
```

The `setContainerNameConfig()` method (lines 244-298) writes `{container-name}.json` to platform-specific path:

- macOS: `~/Library/Application Support/Code/User/globalStorage/ms-vscode-remote.remote-containers/nameConfigs/`
- Windows: `%APPDATA%\Code\User\globalStorage\ms-vscode-remote.remote-containers\nameConfigs\`
- Linux: `~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/nameConfigs/`

Config content:

```json
{"workspaceFolder": "/workspace/base-build", "remoteUser": "root"}
```

### Testing & Verification

Tested on macOS - config file created correctly and VSCode opens `/workspace/base-build` directly.

**Windows troubleshooting:** Check if config file exists at `%APPDATA%\Code\User\globalStorage\ms-vscode-remote.remote-containers\nameConfigs\{container}.json`. Verify content has correct `workspaceFolder`. Check extension output for "Written nameConfig" log. Note: VSCode Insiders uses `Code - Insiders` instead of `Code` in path.

\> - 不是以项目的方式进入的，没有进入项目目录 > > <img width="637" alt="9f176ffeadcea380426f042fea79b947.png" src="attachments/edc58f00-0d1e-403a-956d-f53217061679"> ## Auto-Open Workspace Folder ### Problem "Attach to Running Container" opens root directory (\`/\`) instead of project workspace (\`/workspace/reponame\`). ### Server-side (docker\_agent.go lines 315-321) Three Docker labels are set on container creation. The \`devcontainer.metadata\` label is key - Dev Containers extension reads \`workspaceFolder\` from it: \`\`\`go devcontainerMetadata:= fmt.Sprintf(\`\[{"remoteUser":"root","workspaceFolder":"%s/%s"}\]\`, containerWorkspaceDir, repo.Name) startCommand += fmt.Sprintf(\` --label 'devcontainer.metadata=%s' \`, devcontainerMetadata) \`\`\` ### Client-side (devstar-vscode extension) Dev Containers extension reads per-container settings from \`nameConfigs\` directory. Our extension creates config file before \`attachToRunningContainer\`: \`\`\`typescript // src/remote-container.ts lines 205-213 const workspaceFolder = \`/workspace/${repoName}\`; await this.setContainerNameConfig(containerName, workspaceFolder); // Write config first await vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName); \`\`\` The \`setContainerNameConfig()\` method (lines 244-298) writes \`{container-name}.json\` to platform-specific path: - macOS: \`~/Library/Application Support/Code/User/globalStorage/ms-vscode-remote.remote-containers/nameConfigs/\` - Windows: \`%APPDATA%\\Code\\User\\globalStorage\\ms-vscode-remote.remote-containers\\nameConfigs\\\` - Linux: \`~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/nameConfigs/\` Config content: \`\`\`json {"workspaceFolder": "/workspace/base-build", "remoteUser": "root"} \`\`\` ### Testing & Verification Tested on macOS - config file created correctly and VSCode opens \`/workspace/base-build\` directly. \*\*Windows troubleshooting:\*\* Check if config file exists at \`%APPDATA%\\Code\\User\\globalStorage\\ms-vscode-remote.remote-containers\\nameConfigs\\{container}.json\`. Verify content has correct \`workspaceFolder\`. Check extension output for "Written nameConfig" log. Note: VSCode Insiders uses \`Code - Insiders\` instead of \`Code\` in path.

于

上个月

推送 1 个提交

于

上个月

推送 2 个提交

[refactor: unify SSHWorkspacePath and UserWorkspaceBasePath into single config](https://www.devstar.cn/devstar/devstar/commit/3d8ef178079906c404551e8de1daefd21228e261) [3d8ef17807](https://www.devstar.cn/devstar/devstar/commit/3d8ef178079906c404551e8de1daefd21228e261)

[feat: make default devcontainer image configurable via app.ini](https://www.devstar.cn/devstar/devstar/commit/c0fb390cf70302691daec16761638c746aebe4a0) [c0fb390cf7](https://www.devstar.cn/devstar/devstar/commit/c0fb390cf70302691daec16761638c746aebe4a0)

### 02cd696 refactor: unify SSHWorkspacePath and UserWorkspaceBasePath into single config

Previously there were two similar config fields for workspace paths:

- `SSHWorkspacePath` = `/var/lib/gitea/devstar-workspace` (used in URL generation and workspace\_prepare.go)
- `UserWorkspaceBasePath` = `/var/lib/gitea/user-workspace` (used in docker volume mount)

This was confusing and redundant. Unified them into a single `UserWorkspaceBasePath` config.

**Changes in `modules/setting/devcontainer.go`:**

- Removed `SSHWorkspacePath` field from struct
- Removed `SSH_WORKSPACE_PATH` config loading

**Changes in `services/devcontainer/workspace_prepare.go`:**

```markup
// Before:
workspacePath := setting.DevContainerConfig.SSHWorkspacePath
// After:
workspacePath := setting.DevContainerConfig.UserWorkspaceBasePath
```

**Changes in `services/devcontainer/devcontainer.go`:**

- Updated log message and URL parameter to use `UserWorkspaceBasePath`

### bcd3296 feat: make default devcontainer image configurable via app.ini

The default devcontainer image `mcr.microsoft.com/devcontainers/base:ubuntu` was hardcoded in two places. Now it's configurable via `app.ini`.

**Changes in `modules/setting/devcontainer.go`:**

```markup
// Added new field
DefaultImage string // 默认 devcontainer 镜像

// Loading from config
DevContainerConfig.DefaultImage = sec.Key("DEFAULT_IMAGE").MustString("mcr.microsoft.com/devcontainers/base:ubuntu")
```

**Changes in `services/devcontainer/devcontainer.go` and `routers/api/devcontainer/devcontainer.go`:**

```markup
// Before:
imageName := "mcr.microsoft.com/devcontainers/base:ubuntu"
// After:
imageName := setting.DevContainerConfig.DefaultImage
```

**Configuration example (app.ini):**

```markup
[devcontainer]
DEFAULT_IMAGE = mcr.microsoft.com/devcontainers/base:ubuntu
```

\### \`02cd696\` refactor: unify SSHWorkspacePath and UserWorkspaceBasePath into single config Previously there were two similar config fields for workspace paths: - \`SSHWorkspacePath\` = \`/var/lib/gitea/devstar-workspace\` (used in URL generation and workspace\_prepare.go) - \`UserWorkspaceBasePath\` = \`/var/lib/gitea/user-workspace\` (used in docker volume mount) This was confusing and redundant. Unified them into a single \`UserWorkspaceBasePath\` config. \*\*Changes in \`modules/setting/devcontainer.go\`:\*\* - Removed \`SSHWorkspacePath\` field from struct - Removed \`SSH\_WORKSPACE\_PATH\` config loading \*\*Changes in \`services/devcontainer/workspace\_prepare.go\`:\*\* \`\`\`go // Before: workspacePath:= setting.DevContainerConfig.SSHWorkspacePath // After: workspacePath:= setting.DevContainerConfig.UserWorkspaceBasePath \`\`\` \*\*Changes in \`services/devcontainer/devcontainer.go\`:\*\* - Updated log message and URL parameter to use \`UserWorkspaceBasePath\` ### \`bcd3296\` feat: make default devcontainer image configurable via app.ini The default devcontainer image \`mcr.microsoft.com/devcontainers/base:ubuntu\` was hardcoded in two places. Now it's configurable via \`app.ini\`. \*\*Changes in \`modules/setting/devcontainer.go\`:\*\* \`\`\`go // Added new field DefaultImage string // 默认 devcontainer 镜像 // Loading from config DevContainerConfig.DefaultImage = sec.Key("DEFAULT\_IMAGE").MustString("mcr.microsoft.com/devcontainers/base:ubuntu") \`\`\` \*\*Changes in \`services/devcontainer/devcontainer.go\` and \`routers/api/devcontainer/devcontainer.go\`:\*\* \`\`\`go // Before: imageName:= "mcr.microsoft.com/devcontainers/base:ubuntu" // After: imageName:= setting.DevContainerConfig.DefaultImage \`\`\` \*\*Configuration example (app.ini):\*\* \`\`\`ini \[devcontainer\] DEFAULT\_IMAGE = mcr.microsoft.com/devcontainers/base:ubuntu \`\`\`

### 测试状态 ✅ 通过 (Passed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ✅ 通过 (Passed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于

上个月

推送 1 个提交

[Merge branch 'main' into feat/ssh-refactor](https://www.devstar.cn/devstar/devstar/commit/63e70d6c416bca56e757242c7db733e088d2e0c0) [63e70d6c41](https://www.devstar.cn/devstar/devstar/commit/63e70d6c416bca56e757242c7db733e088d2e0c0)

```markup
log.ts:440  INFO Invoking resolveAuthority(attached-container)...
log.ts:440  INFO [LocalProcess0][resolveAuthority(attached-container,1)][0ms] obtaining proxy...
log.ts:440  INFO Started local extension host with pid 17988.
log.ts:440  INFO MCP Registry configured: https://api.mcp.github.com
log.ts:440  INFO [LocalProcess0][resolveAuthority(attached-container,1)][827ms] invoking...
log.ts:460   ERR navigator is now a global in nodejs, please see https://aka.ms/vscode-extensions/navigator for additional info on this error.: PendingMigrationError: navigator is now a global in nodejs, please see https://aka.ms/vscode-extensions/navigator for additional info on this error.
    at get (file:///d:/Programs/Microsoft%20VS%20Code/resources/app/out/vs/workbench/api/node/extensionHostProcess.js:405:6684)
    at vt (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:11229)
    at Gn (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:7601)
    at c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:11074
    at gu (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:7625)
    at c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:22:3161
    at Object.l [as use] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:13883)
    at yde (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:14787)
    at Object.l [as watch] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:15016)
    at hr (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:15736)
    at V.<computed> [as initialize] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:22:2663)
    at t.u [as initialize] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:20556)
    at c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:22:13725
    at mn (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:23793)
    at W.<computed> [as initialize] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:22:13120)
    at e.u [as initialize] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:20556)
    at Array.<anonymous> (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:27032)
    at ee (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:12439)
    at XL (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:26996)
    at Be (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:41335)
    at N.<computed> (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:37044)
    at Object.initialize (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:19857)
    at c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:54646
    at mn (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:23793)
    at r.<computed> [as initialize] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:20:54574)
    at e.u [as initialize] (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:19:20556)
    at Fme (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:293:3630)
    at async C6 (c:\Users\mengn\.vscode\extensions\ms-vscode-remote.remote-containers-0.437.0\dist\extension\extension.js:293:3857)
error @ log.ts:460
log.ts:440  INFO [LocalProcess0][resolveAuthority(attached-container,1)][1828ms] waiting...
log.ts:440  INFO [LocalProcess0][resolveAuthority(attached-container,1)][2828ms] waiting...
log.ts:440  INFO [LocalProcess0][resolveAuthority(attached-container,1)][3828ms] waiting...
log.ts:440  INFO [LocalProcess0][resolveAuthority(attached-container,1)][4760ms] returned WebSocket(127.0.0.1:42793)
log.ts:440  INFO resolveAuthority(attached-container) returned 'WebSocket(127.0.0.1:42793)' after 4760 ms
log.ts:440  INFO Creating a socket (renderer-Management-7e7ebb94-82ac-4e7b-b051-41caa0e8b203)...
log.ts:440  INFO Creating a socket (renderer-ExtensionHost-b5be6bbe-4e14-48bc-815a-1b08e2374017)...
log.ts:440  INFO Creating a socket (renderer-Management-7e7ebb94-82ac-4e7b-b051-41caa0e8b203) was successful after 155 ms.
log.ts:440  INFO [reconnection-grace-time] Client received grace time from server: 10800000ms (10800s)
log.ts:440  INFO Creating a socket (renderer-ExtensionHost-b5be6bbe-4e14-48bc-815a-1b08e2374017) was successful after 530 ms.
log.ts:440  INFO Settings Sync: Account status changed from uninitialized to unavailable
log.ts:440  INFO [perf] Render performance baseline is 26ms
api.github.com/copilot/mcp_registry:1  Failed to load resource: the server responded with a status of 404 ()
log.ts:460   ERR Failed to fetch MCP registry providers Server returned 404
error @ log.ts:460
log.ts:450  WARN [perf] Renderer reported VERY LONG TASK (394ms), starting profiling session '30189bfb-b7f0-4c4a-a2b6-9ed9217f5507'
warn @ log.ts:450
log.ts:460   ERR [Extension Host] (node:423) [DEP0040] DeprecationWarning: The \`punycode\` module is deprecated. Please use a userland alternative instead.
(Use \`node --trace-deprecation ...\` to show where the warning was created)
error @ log.ts:460
console.ts:139 [Extension Host] (node:423) [DEP0040] DeprecationWarning: The \`punycode\` module is deprecated. Please use a userland alternative instead.
(Use \`node --trace-deprecation ...\` to show where the warning was created)
jxs @ console.ts:139
log.ts:460   ERR [Extension Host] (node:423) ExperimentalWarning: SQLite is an experimental feature and might change at any time
error @ log.ts:460
console.ts:139 [Extension Host] (node:423) ExperimentalWarning: SQLite is an experimental feature and might change at any time
jxs @ console.ts:139
log.ts:460   ERR chatParticipant must be declared in package.json: claude-code
error @ log.ts:460
```

- 只是进入了容器，没有打开项目，进入项目目录下

\`\`\` log.ts:440 INFO Invoking resolveAuthority(attached-container)... log.ts:440 INFO \[LocalProcess0\]\[resolveAuthority(attached-container,1)\]\[0ms\] obtaining proxy... log.ts:440 INFO Started local extension host with pid 17988. log.ts:440 INFO MCP Registry configured: https://api.mcp.github.com log.ts:440 INFO \[LocalProcess0\]\[resolveAuthority(attached-container,1)\]\[827ms\] invoking... log.ts:460 ERR navigator is now a global in nodejs, please see https://aka.ms/vscode-extensions/navigator for additional info on this error.: PendingMigrationError: navigator is now a global in nodejs, please see https://aka.ms/vscode-extensions/navigator for additional info on this error. at get (file:///d:/Programs/Microsoft%20VS%20Code/resources/app/out/vs/workbench/api/node/extensionHostProcess.js:405:6684) at vt (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:11229) at Gn (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:7601) at c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:11074 at gu (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:7625) at c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:22:3161 at Object.l \[as use\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:13883) at yde (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:14787) at Object.l \[as watch\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:15016) at hr (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:15736) at V.<computed> \[as initialize\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:22:2663) at t.u \[as initialize\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:20556) at c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:22:13725 at mn (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:23793) at W.<computed> \[as initialize\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:22:13120) at e.u \[as initialize\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:20556) at Array.<anonymous> (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:27032) at ee (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:12439) at XL (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:26996) at Be (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:41335) at N.<computed> (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:37044) at Object.initialize (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:19857) at c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:54646 at mn (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:23793) at r.<computed> \[as initialize\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:20:54574) at e.u \[as initialize\] (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:19:20556) at Fme (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:293:3630) at async C6 (c:\\Users\\mengn\\.vscode\\extensions\\ms-vscode-remote.remote-containers-0.437.0\\dist\\extension\\extension.js:293:3857) error @ log.ts:460 log.ts:440 INFO \[LocalProcess0\]\[resolveAuthority(attached-container,1)\]\[1828ms\] waiting... log.ts:440 INFO \[LocalProcess0\]\[resolveAuthority(attached-container,1)\]\[2828ms\] waiting... log.ts:440 INFO \[LocalProcess0\]\[resolveAuthority(attached-container,1)\]\[3828ms\] waiting... log.ts:440 INFO \[LocalProcess0\]\[resolveAuthority(attached-container,1)\]\[4760ms\] returned WebSocket(127.0.0.1:42793) log.ts:440 INFO resolveAuthority(attached-container) returned 'WebSocket(127.0.0.1:42793)' after 4760 ms log.ts:440 INFO Creating a socket (renderer-Management-7e7ebb94-82ac-4e7b-b051-41caa0e8b203)... log.ts:440 INFO Creating a socket (renderer-ExtensionHost-b5be6bbe-4e14-48bc-815a-1b08e2374017)... log.ts:440 INFO Creating a socket (renderer-Management-7e7ebb94-82ac-4e7b-b051-41caa0e8b203) was successful after 155 ms. log.ts:440 INFO \[reconnection-grace-time\] Client received grace time from server: 10800000ms (10800s) log.ts:440 INFO Creating a socket (renderer-ExtensionHost-b5be6bbe-4e14-48bc-815a-1b08e2374017) was successful after 530 ms. log.ts:440 INFO Settings Sync: Account status changed from uninitialized to unavailable log.ts:440 INFO \[perf\] Render performance baseline is 26ms api.github.com/copilot/mcp\_registry:1 Failed to load resource: the server responded with a status of 404 () log.ts:460 ERR Failed to fetch MCP registry providers Server returned 404 error @ log.ts:460 log.ts:450 WARN \[perf\] Renderer reported VERY LONG TASK (394ms), starting profiling session '30189bfb-b7f0-4c4a-a2b6-9ed9217f5507' warn @ log.ts:450 log.ts:460 ERR \[Extension Host\] (node:423) \[DEP0040\] DeprecationWarning: The \`punycode\` module is deprecated. Please use a userland alternative instead. (Use \`node --trace-deprecation...\` to show where the warning was created) error @ log.ts:460 console.ts:139 \[Extension Host\] (node:423) \[DEP0040\] DeprecationWarning: The \`punycode\` module is deprecated. Please use a userland alternative instead. (Use \`node --trace-deprecation...\` to show where the warning was created) jxs @ console.ts:139 log.ts:460 ERR \[Extension Host\] (node:423) ExperimentalWarning: SQLite is an experimental feature and might change at any time error @ log.ts:460 console.ts:139 \[Extension Host\] (node:423) ExperimentalWarning: SQLite is an experimental feature and might change at any time jxs @ console.ts:139 log.ts:460 ERR chatParticipant must be declared in package.json: claude-code error @ log.ts:460 \`\`\` - 只是进入了容器，没有打开项目，进入项目目录下

### 测试状态 ✅ 通过 (Passed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ✅ 通过 (Passed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

### 测试状态 ✅ 通过 (Passed)

- 列出有效的信息，尤其是失败的时候的错误信息

---

> *此评论由 DevStar Actions 自动生成，用于 PR 质量检查。*

\### 测试状态 ✅ 通过 (Passed) - 列出有效的信息，尤其是失败的时候的错误信息 --- > \*此评论由 DevStar Actions 自动生成，用于 PR 质量检查。\*

于

上个月

修改标题 **~~WIP: feat: Add unified SSH entry point for IDE integration via Docker over SSH~~** 为 **feat: Add unified SSH entry point for IDE integration via Docker over SSH**

于

上个月

合并提交 [**9319ee9436**](https://www.devstar.cn/devstar/devstar/commit/9319ee9436546b4f13362f3b2eda519f03bd9e61) 到 **main**

于[

上个月

](https://www.devstar.cn/devstar/devstar/pulls/108#event-1692)在代码提交中引用该工单

[feat: Add unified SSH entry point for IDE integration via Docker over SSH (#108)](https://www.devstar.cn/devstar/devstar/commit/9319ee9436546b4f13362f3b2eda519f03bd9e61)

于

上个月

删除分支 **feat/ssh-refactor**

于[

2周前

](https://www.devstar.cn/devstar/devstar/pulls/108#event-1982)[引用合并请求](https://www.devstar.cn/devstar/devstar/issues/145)

[**SSH public key not injected into DevContainers, IDE connection broken** #145](https://www.devstar.cn/devstar/devstar/issues/145)

## DevStar "Open with VSCode" — Docker-over-SSH Connection Architecture

> Full-stack technical document covering the end-to-end flow from clicking "Open with VSCode" in the DevStar Web UI to attaching VSCode to a remote dev container via Docker-over-SSH.

---

1. [Architecture Overview](https://www.devstar.cn/devstar/devstar/pulls/108#1-architecture-overview)
2. [System Components](https://www.devstar.cn/devstar/devstar/pulls/108#2-system-components)
3. [End-to-End Connection Flow](https://www.devstar.cn/devstar/devstar/pulls/108#3-end-to-end-connection-flow)
4. [SSH Key Lifecycle](https://www.devstar.cn/devstar/devstar/pulls/108#4-ssh-key-lifecycle)
5. [Docker-over-SSH Proxy](https://www.devstar.cn/devstar/devstar/pulls/108#5-docker-over-ssh-proxy)
6. [Dev Container Creation & Volume Mounts](https://www.devstar.cn/devstar/devstar/pulls/108#6-dev-container-creation--volume-mounts)
7. [VSCode Plugin Internals](https://www.devstar.cn/devstar/devstar/pulls/108#7-vscode-plugin-internals)
8. [Security Model](https://www.devstar.cn/devstar/devstar/pulls/108#8-security-model)
9. [Platform-Specific Considerations](https://www.devstar.cn/devstar/devstar/pulls/108#9-platform-specific-considerations)
10. [Sequence Diagram](https://www.devstar.cn/devstar/devstar/pulls/108#10-sequence-diagram)

---

## 1\. Architecture Overview

DevStar uses a **Docker-over-SSH** approach to let users open remote dev containers in VSCode. The key idea: VSCode's Docker CLI connects to the DevStar server's Docker daemon **through an SSH tunnel**, then the Dev Containers extension attaches to the running container.

**Why not direct SSH into the container?**

Traditional approaches SSH directly into the dev container. DevStar instead routes Docker API commands over SSH because:

- DevStar's SSH server is Gitea's built-in SSH (does not provide a shell)
- Docker's `system dial-stdio` command creates a bidirectional API channel over SSH
- Dev Containers extension natively supports Docker-over-SSH via `DOCKER_HOST=ssh://...`
- No need to expose individual container SSH ports to the outside

---

## 2\. System Components

### 2.1 DevStar Server (Backend — Go)

| Component | File | Role |
| --- | --- | --- |
| IDE URL Generator | `services/devcontainer/devcontainer.go` | Generates `vscode://` URI with all connection params |
| SSH Command Router | `cmd/serv.go` | Intercepts SSH commands, routes `docker` commands to proxy |
| Docker Command Proxy | `cmd/serv.go` (`runDockerCommand`) | Validates and proxies Docker CLI commands to local daemon |
| SSH Server | `modules/ssh/ssh.go` | Handles SSH authentication, key verification, session management |
| Container Manager | `services/devcontainer/docker_agent.go` | Creates/manages dev containers via Docker API |
| Key Management | `routers/api/v1/user/key.go` | API endpoint for public key upload |
| authorized\_keys | `services/asymkey/ssh_key_authorized_keys.go` | Regenerates SSH authorized\_keys file |

### 2.2 DevStar Web Frontend

| Component | File | Role |
| --- | --- | --- |
| IDE Button Renderer | `routers/web/devcontainer/devcontainer.go` | Renders "Open with VSCode" buttons with correct URLs |
| URL Template | `modules/setting/config.go` | Defines IDE URL template with parameter placeholders |

### 2.3 VSCode Plugin (TypeScript)

| Component | File | Role |
| --- | --- | --- |
| URI Handler | `src/main.ts` | Receives `vscode://` URI, parses params, stores in globalState |
| Connection Manager | `src/remote-container.ts` | Orchestrates SSH setup, Docker context, container attachment |
| User/Key Manager | `src/user.ts` | Generates RSA key pairs, manages SSH keys |
| API Handler | `src/devstar-api.ts` | Communicates with DevStar REST API (key upload, container status) |

---

## 3\. End-to-End Connection Flow

### Phase 1: URL Generation (Server → Browser)

1. User visits a repository page on DevStar and clicks **"Open with VSCode"**
2. Server calls `Get_IDE_TerminalURL()` which:
	- Looks up the dev container record from the database
		- Generates a one-time `access_token` (stored as `terminal_login_token`)
		- Checks if SSH unified mode is enabled (`setting.DevContainerConfig.SSHEnabled`)
		- Builds the URL from the configured template:

```markup
vscode://mengning.devstar/openProject?
  host={repoName}
  &hostname={serverDomain}
  &port={sshPort}
  &username={sshUser}
  &path={workspacePath}
  &access_token={token}
  &devstar_username={userName}
  &devstar_domain={serverURL}
  &sshUnified=true                          ← Unified SSH flag
  &containerName={sanitizedContainerName}   ← Server-generated name
  &workspacePath={baseWorkspacePath}        ← Base path on host
```

1. Browser triggers the `vscode://` protocol handler, which opens VSCode

### Phase 2: URI Handling (VSCode Plugin)

1. VSCode receives the URI → `main.ts` URI handler activates
2. Parses all query parameters via `URLSearchParams`
3. Stores unified SSH params in `globalState`:
	- `sshUnified: true`
		- `devstarUsername: "alice"`
		- `containerName: "alice-orgname-reponame"`
		- `workspacePath: "/var/lib/gitea/user-workspace"`
4. Handles user authentication:
	- New user: auto-login with the `access_token`
		- Existing user (same account): proceed directly
		- Different user: prompt to switch or continue
5. Calls `remoteContainer.firstOpenProject()`

### Phase 3: SSH Key Setup (VSCode Plugin)

1. `firstOpenProject()` reads `sshUnified=true` from `globalState` → enters `firstConnectUnified()`
2. **Container status check**: API call to `GET /api/v1/devcontainer/status` — verifies container is running
3. **SSH key pair generation** (if not exists):
	- Algorithm: RSA 4096-bit
		- Format: PKCS1 PEM (private), OpenSSH (public)
		- Path: `~/.ssh/id_rsa_{username}_{hostname}` and `.pub`
		- Permissions: `0o600` (Unix) or `icacls` restricted (Windows)
4. **Public key upload**: `POST /api/v1/user/keys` → server stores in database
5. **SSH config update**: Writes entry to `~/.ssh/config`:
	```markup
	Host devstar-remote-orgname-reponame
	  HostName devstar.cn
	  Port 22
	  User git
	  PreferredAuthentications publickey
	  IdentityFile ~/.ssh/id_rsa_alice_devstar_cn
	  StrictHostKeyChecking no
	  UserKnownHostsFile /dev/null
	```
6. **ssh-agent**: Runs `ssh-add ~/.ssh/id_rsa_alice_devstar_cn` to load key into agent
	- Docker CLI uses ssh-agent for authentication (does not read SSH config's IdentityFile)

### Phase 4: Docker Context & Environment (VSCode Plugin)

1. **Save original Docker config** for later restoration:
	- Current Docker context (`docker context show`)
		- Current `containers.environment` from settings.json
2. **Create Docker context**:
	```bash
	docker context create "devstar-remote-orgname-reponame" \
	  --docker "host=ssh://devstar-remote-orgname-reponame"
	docker context use "devstar-remote-orgname-reponame"
	```
3. **Set `containers.environment.DOCKER_HOST`** in VSCode `settings.json`:
	```json
	{
	  "containers.environment": {
	    "DOCKER_HOST": "ssh://devstar-remote-orgname-reponame"
	  }
	}
	```
	**Why both Docker context AND environment variable?**
	- Docker context: controls what the Docker CLI connects to
		- `containers.environment.DOCKER_HOST`: tells the Dev Containers extension to use Docker CLI (via `dial-stdio`) instead of trying to SSH into the host for environment detection. Without this, Dev Containers would attempt to open a shell on the SSH host — which Gitea's SSH server does not support.

### Phase 5: Container Attachment (VSCode Plugin → Dev Containers Extension)

1. **Write nameConfig**: Creates `{containerName}.json` in Dev Containers' `nameConfigs/` directory:
	```json
	{
	  "workspaceFolder": "/workspace/reponame",
	  "remoteUser": "root"
	}
	```
	This tells Dev Containers what folder to open and which user to use when attaching.
2. **Set up port forwarding** (if `forwardPorts` specified):
	- Creates SSH tunnels: `ssh -N -L {localPort}:localhost:{containerPort} ...`
		- Each tunnel runs as a detached child process
		- Tracked for cleanup on extension deactivation
3. **Attach to container**:
	```markup
	vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName)
	```
	Dev Containers extension:
	- Reads `DOCKER_HOST=ssh://...` from `containers.environment`
		- Runs `docker system dial-stdio` over SSH to establish API channel
		- Finds the container by name
		- Attaches VSCode to the container (installs VS Code Server inside, opens workspace)

### Phase 6: Cleanup (VSCode Plugin)

1. **Deferred restoration** (60 seconds after attachment):
	- Restores original Docker context
		- Restores original `containers.environment` in settings.json
2. **globalState cleanup**: Clears `sshUnified`, `devstarUsername`, `containerName`, `workspacePath`
3. **On error**: Immediately restores Docker config before throwing

---

## 4\. SSH Key Lifecycle

### 4.1 Key Generation (Client-Side)

Key naming convention: `id_rsa_alice_devstar_cn` (dots and colons in hostname replaced with underscores).

### 4.2 Key Upload (Client → Server)

### 4.3 Key Injection into Running Containers

When a new public key is uploaded, the server calls `AddPublicKeyToAllRunningDevContainer()`:

```markup
// For each running container owned by this user:
docker exec {containerName} sh -c "echo '{publicKey}' >> ~/.ssh/authorized_keys"
```

This ensures existing containers immediately accept the new key without restart.

### 4.4 Key Usage During Connection

The Docker CLI connects to `ssh://devstar-remote-xxx` using the ssh-agent-loaded key. DevStar's SSH server authenticates the key and routes the Docker command.

### 4.5 Key Storage Locations Summary

| Location | What | Who Writes | Who Reads |
| --- | --- | --- | --- |
| `~/.ssh/id_rsa_{u}_{h}` | Private key | Plugin | ssh-agent → Docker CLI |
| `~/.ssh/id_rsa_{u}_{h}.pub` | Public key | Plugin | Plugin (for upload) |
| `~/.ssh/config` | SSH host alias | Plugin | Docker CLI (host resolution) |
| Server DB `public_key` table | Public key record | Server API | SSH auth |
| Server `{SSH.RootPath}/authorized_keys` | All public keys | Server | SSH daemon (sshd/built-in) |
| Container `~/.ssh/authorized_keys` | User's public keys | Server (docker exec) | Container's sshd |

---

## 5\. Docker-over-SSH Proxy

### 5.1 How It Works

When the Docker CLI is configured with `DOCKER_HOST=ssh://...`, it:

1. Opens an SSH connection to the specified host
2. Sends the command `docker system dial-stdio` over SSH
3. This establishes a bidirectional byte stream (stdin/stdout) that carries Docker API requests/responses
4. The Docker CLI sends HTTP API calls through this stream, just as it would over a local Unix socket

### 5.2 Server-Side Command Routing

### 5.3 system dial-stdio Deep Dive

This is the critical command that enables VSCode's Docker-over-SSH:

The `dial-stdio` command opens a raw connection to the Docker daemon socket (`/var/run/docker.sock`) and bridges it to SSH's stdin/stdout. This allows the remote Docker CLI to communicate with the daemon as if it were local.

---

## 6\. Dev Container Creation & Volume Mounts

### 6.1 Container Creation

File: `services/devcontainer/docker_agent.go`

When a user creates a dev container, the server:

1. Generates a sanitized container name: `{username}-{owner}-{repo}`
	- Rules: remove non-alphanumeric chars, lowercase, truncate (user: 15, owner: 15, repo: 31)
2. Creates the container with:
	- **Image**: From `.devcontainer/devcontainer.json` or default
		- **Command**: `tail -f /dev/null` (keeps container alive)
		- **Labels**:
		- `devcontainer.local_folder`: `{workspaceDir}/{repoName}`
				- `devcontainer.config_file`: path to `devcontainer.json`
		- **Port exposure**: SSH port 22
3. Runs initialization inside the container:
	- Configures `/etc/hosts` (adds `host.docker.internal`)
		- Installs git and SSH server
		- Clones the repository via HTTP into `/workspace/{repoName}`
		- Generates SSH host keys (`ssh-keygen -A`)
		- Starts SSH service
		- **Injects all of the user's public keys** into `~/.ssh/authorized_keys`

### 6.2 Volume Mounts

| Mount | Host Path | Container Path | Purpose |
| --- | --- | --- | --- |
| **User Workspace** | `/var/lib/gitea/user-workspace/{username}` | `/workspace` | Persistent workspace data across container rebuilds |
| **devcontainer.json Mounts** | User-defined in `.devcontainer/devcontainer.json` | User-defined | Project-specific custom mounts |
| **Docker Socket (WebTerminal only)** | `/var/run/docker.sock` | `/var/run/docker.sock` | DooD — allows WebTerminal to manage containers |

### 6.3 DooD (Docker-outside-of-Docker) Path Consideration

**Important**: DevStar itself runs inside a Docker container with a named volume:

The bind mount path in `-v /var/lib/gitea/user-workspace/alice:/workspace` resolves from the **host's filesystem**, not from DevStar's container filesystem. This is because `docker.sock` talks to the host's Docker daemon directly.

---

## 7\. VSCode Plugin Internals

### 7.1 firstOpenProject() — Entry Point Decision

```typescript
// remote-container.ts, line 89
async firstOpenProject(host, hostname, port, username, path, context) {
  const sshUnified = context.globalState.get('sshUnified');      // true/false
  const devstarUsername = context.globalState.get('devstarUsername');

  if (sshUnified && devstarUsername) {
    // ──► Unified Docker-over-SSH path (NEW)
    const containerName = context.globalState.get('containerName')
      || this.generateContainerName(devstarUsername, owner, repo);
    await this.firstConnectUnified(host, hostname, port, username, path, containerName, context);
    return;
  }

  if (vscode.env.remoteName) {
    // ──► Remote window: delegate to local window via code --open-url (LEGACY)
    ...
  } else {
    // ──► Local window: direct SSH connection (LEGACY)
    ...
  }
}
```

### 7.2 Docker Context Management

The plugin creates a **named Docker context** to override Docker Desktop's default `desktop-linux` context (which forces connections to the local Docker daemon):

```bash
# Create context pointing to remote Docker via SSH
docker context create "devstar-remote-xxx" --docker "host=ssh://devstar-remote-xxx"

# Switch to it
docker context use "devstar-remote-xxx"
```

After the connection is established (60s delay), the original context is restored:

```bash
docker context use "desktop-linux"   # or whatever was original
```

### 7.3 containers.environment.DOCKER\_HOST

This VSCode setting is written to `settings.json` to control how the **Dev Containers extension** connects:

```json
{
  "containers.environment": {
    "DOCKER_HOST": "ssh://devstar-remote-xxx"
  }
}
```

**Why is this needed in addition to Docker context?**

When Dev Containers detects an SSH-type Docker context, it tries to SSH into the host and open a `/bin/sh` shell to detect the environment (OS, architecture, etc.). DevStar's Gitea SSH server does **not** support shell access — it only supports `git` and `docker` commands.

Setting `DOCKER_HOST` in `containers.environment` forces Dev Containers to use Docker CLI commands (which go through `dial-stdio`) instead of attempting shell access. This is the key insight that makes the whole architecture work.

### 7.4 nameConfigs — Workspace Folder Mapping

Dev Containers needs to know what folder to open when attaching to a container. This is configured via a JSON file:

```markup
~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/nameConfigs/{containerName}.json
```

Content:

```json
{
  "workspaceFolder": "/workspace/my-repo",
  "remoteUser": "root"
}
```

### 7.5 Port Forwarding

For each port in the `forwardPorts` URL parameter, the plugin creates an SSH tunnel:

```bash
ssh -N -L {localPort}:localhost:{containerPort} \
    -p {sshPort} -i {keyPath} \
    -o StrictHostKeyChecking=no \
    root@{hostname}
```

Tunnels are:

- Created as detached child processes
- Tracked in `sshTunnelProcesses[]` for cleanup
- Killed on extension deactivation (`dispose()`)

---

## 8\. Security Model

### 8.1 Authentication Chain

### 8.2 Docker Command Whitelist

Only these Docker subcommands are allowed through the SSH proxy:

| Command | Purpose |
| --- | --- |
| `ps` | List containers |
| `inspect` | Get container details |
| `exec` | Execute commands in container |
| `start` / `stop` | Container lifecycle |
| `attach` | Attach to container (for Dev Containers) |
| `logs` | View container logs |
| `version` / `info` | Docker daemon info |
| `system` | Required for `dial-stdio` |

Commands like `run`, `rm`, `build`, `pull`, `push` are **not allowed**.

### 8.3 Container Namespace Isolation

```markup
// cmd/serv.go — runDockerCommand()
sanitizedUsername := sanitizeUsername(user.Name)  // e.g., "alice"
if !strings.HasPrefix(containerName, sanitizedUsername + "-") {
    return "Access denied: You can only access your own containers"
}
```

User `alice` can only interact with containers named `alice-*`. This prevents cross-user container access even if someone crafts a malicious Docker command.

### 8.4 SSH Key Security

- Private key: `0o600` permissions (owner read/write only)
- Windows: `icacls` restricts to current user
- `StrictHostKeyChecking no` — trusts server identity (acceptable for managed infrastructure)
- ssh-agent used for key authentication (key not written to Docker config)

---

## 9\. Platform-Specific Considerations

### 9.1 File Path Matrix

| Item | macOS | Linux | Windows | WSL |
| --- | --- | --- | --- | --- |
| SSH keys | `~/.ssh/` | `~/.ssh/` | `%USERPROFILE%\.ssh\` | `~/.ssh/` (WSL home) |
| SSH config | `~/.ssh/config` | `~/.ssh/config` | `%USERPROFILE%\.ssh\config` | `~/.ssh/config` |
| VSCode settings | `~/Library/.../settings.json` | `~/.config/Code/.../settings.json` | `%APPDATA%\Code\...\settings.json` | ⚠️ See below |
| nameConfigs | `~/Library/.../nameConfigs/` | `~/.config/Code/.../nameConfigs/` | `%APPDATA%\Code\...\nameConfigs\` | ⚠️ See below |

### 9.2 WSL Known Issues

When VSCode is in **WSL Remote** mode, the extension host runs inside WSL, but the Dev Containers extension runs on the **Windows side**:

| Problem | Cause | Status |
| --- | --- | --- |
| `docker` CLI not found | Docker Desktop WSL integration not enabled, or `docker.exe` not in PATH | Needs fix: fallback to `docker.exe` |
| `containers.environment` write fails | Dev Containers extension schema not visible from WSL extension host | Needs fix: use file-write to Windows-side path |
| Settings written to wrong path | `~/.config/Code/...` is WSL path; Dev Containers reads from Windows `%APPDATA%` | Needs fix: detect WSL and resolve Windows path |
| `dev.containers.executeInWSL` | Currently forced to `false`; should be `true` so Docker commands route through WSL where SSH is configured | Needs fix |

### 9.3 Windows-Specific

- SSH key permissions set via `icacls` instead of `chmod`
- Terminal detection: PowerShell/CMD detected by shell path containing `\`, `powershell`, `pwsh`, or `cmd`
- `code --open-url` uses single-quote wrapping for URL: `'"url"'`

---

## 10\. Sequence Diagram

---

## Appendix: Configuration Reference

### Server-Side Settings (app.ini)

```markup
[devcontainer]
SSH_ENABLED = true                                        ; Enable unified SSH entry
SSH_PORT = 22                                             ; SSH port for Docker-over-SSH
USER_WORKSPACE_BASE_PATH = /var/lib/gitea/user-workspace  ; Host path for workspace volumes
CONTAINER_WORKSPACE_DIR = /workspace                      ; Container-side workspace mount point
```

### IDE URL Template (modules/setting/config.go)

```markup
vscode://mengning.devstar/openProject?
  host={host}&hostname={hostname}&port={port}&username={username}&path={path}
  &access_token={token}&devstar_username={devstar_username}&devstar_domain={domain}
  &sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath}
```

### Container Naming Convention

```markup
Format:  {sanitized_username}-{sanitized_owner}-{sanitized_repo}
Rules:   [^a-zA-Z0-9] removed, lowercased
Limits:  username(15) - owner(15) - repo(31)
Example: alice-myorg-myproject
```

Both server (`getSanitizedDevcontainerName`) and plugin (`generateContainerName`) use identical logic to ensure the container name matches.

\# DevStar "Open with VSCode" — Docker-over-SSH Connection Architecture > Full-stack technical document covering the end-to-end flow from clicking "Open with VSCode" in the DevStar Web UI to attaching VSCode to a remote dev container via Docker-over-SSH. --- ## Table of Contents 1. \[Architecture Overview\](#1-architecture-overview) 2. \[System Components\](#2-system-components) 3. \[End-to-End Connection Flow\](#3-end-to-end-connection-flow) 4. \[SSH Key Lifecycle\](#4-ssh-key-lifecycle) 5. \[Docker-over-SSH Proxy\](#5-docker-over-ssh-proxy) 6. \[Dev Container Creation & Volume Mounts\](#6-dev-container-creation--volume-mounts) 7. \[VSCode Plugin Internals\](#7-vscode-plugin-internals) 8. \[Security Model\](#8-security-model) 9. \[Platform-Specific Considerations\](#9-platform-specific-considerations) 10. \[Sequence Diagram\](#10-sequence-diagram) --- ## 1. Architecture Overview DevStar uses a \*\*Docker-over-SSH\*\* approach to let users open remote dev containers in VSCode. The key idea: VSCode's Docker CLI connects to the DevStar server's Docker daemon \*\*through an SSH tunnel\*\*, then the Dev Containers extension attaches to the running container. \`\`\`mermaid graph LR subgraph Local\["User's Local Machine"\] VSCode\["VSCode<br/>+ Dev Containers Extension<br/>+ DevStar Plugin"\] end subgraph Server\["DevStar Server"\] SSH\["Gitea SSH Server<br/>(cmd/serv.go)"\] Docker\["Docker Daemon<br/>(/var/run/docker.sock)"\] DevContainer\["Dev Container<br/>(alice-org-repo)"\] SSH -->|"docker system<br/>dial-stdio"| Docker Docker -->|manages| DevContainer end VSCode <-->|"SSH Tunnel<br/>(RSA 4096-bit key auth)"| SSH \`\`\` \*\*Why not direct SSH into the container?\*\* Traditional approaches SSH directly into the dev container. DevStar instead routes Docker API commands over SSH because: - DevStar's SSH server is Gitea's built-in SSH (does not provide a shell) - Docker's \`system dial-stdio\` command creates a bidirectional API channel over SSH - Dev Containers extension natively supports Docker-over-SSH via \`DOCKER\_HOST=ssh://...\` - No need to expose individual container SSH ports to the outside --- ## 2. System Components ### 2.1 DevStar Server (Backend — Go) | Component | File | Role | |-----------|------|------| | IDE URL Generator | \`services/devcontainer/devcontainer.go\` | Generates \`vscode://\` URI with all connection params | | SSH Command Router | \`cmd/serv.go\` | Intercepts SSH commands, routes \`docker\` commands to proxy | | Docker Command Proxy | \`cmd/serv.go\` (\`runDockerCommand\`) | Validates and proxies Docker CLI commands to local daemon | | SSH Server | \`modules/ssh/ssh.go\` | Handles SSH authentication, key verification, session management | | Container Manager | \`services/devcontainer/docker\_agent.go\` | Creates/manages dev containers via Docker API | | Key Management | \`routers/api/v1/user/key.go\` | API endpoint for public key upload | | authorized\_keys | \`services/asymkey/ssh\_key\_authorized\_keys.go\` | Regenerates SSH authorized\_keys file | ### 2.2 DevStar Web Frontend | Component | File | Role | |-----------|------|------| | IDE Button Renderer | \`routers/web/devcontainer/devcontainer.go\` | Renders "Open with VSCode" buttons with correct URLs | | URL Template | \`modules/setting/config.go\` | Defines IDE URL template with parameter placeholders | ### 2.3 VSCode Plugin (TypeScript) | Component | File | Role | |-----------|------|------| | URI Handler | \`src/main.ts\` | Receives \`vscode://\` URI, parses params, stores in globalState | | Connection Manager | \`src/remote-container.ts\` | Orchestrates SSH setup, Docker context, container attachment | | User/Key Manager | \`src/user.ts\` | Generates RSA key pairs, manages SSH keys | | API Handler | \`src/devstar-api.ts\` | Communicates with DevStar REST API (key upload, container status) | --- ## 3. End-to-End Connection Flow ### Phase 1: URL Generation (Server → Browser) 1. User visits a repository page on DevStar and clicks \*\*"Open with VSCode"\*\* 2. Server calls \`Get\_IDE\_TerminalURL()\` which: - Looks up the dev container record from the database - Generates a one-time \`access\_token\` (stored as \`terminal\_login\_token\`) - Checks if SSH unified mode is enabled (\`setting.DevContainerConfig.SSHEnabled\`) - Builds the URL from the configured template: \`\`\` vscode://mengning.devstar/openProject? host={repoName} &hostname={serverDomain} &port={sshPort} &username={sshUser} &path={workspacePath} &access\_token={token} &devstar\_username={userName} &devstar\_domain={serverURL} &sshUnified=true ← Unified SSH flag &containerName={sanitizedContainerName} ← Server-generated name &workspacePath={baseWorkspacePath} ← Base path on host \`\`\` 3. Browser triggers the \`vscode://\` protocol handler, which opens VSCode ### Phase 2: URI Handling (VSCode Plugin) 4. VSCode receives the URI → \`main.ts\` URI handler activates 5. Parses all query parameters via \`URLSearchParams\` 6. Stores unified SSH params in \`globalState\`: - \`sshUnified: true\` - \`devstarUsername: "alice"\` - \`containerName: "alice-orgname-reponame"\` - \`workspacePath: "/var/lib/gitea/user-workspace"\` 7. Handles user authentication: - New user: auto-login with the \`access\_token\` - Existing user (same account): proceed directly - Different user: prompt to switch or continue 8. Calls \`remoteContainer.firstOpenProject()\` ### Phase 3: SSH Key Setup (VSCode Plugin) 9. \`firstOpenProject()\` reads \`sshUnified=true\` from \`globalState\` → enters \`firstConnectUnified()\` 10. \*\*Container status check\*\*: API call to \`GET /api/v1/devcontainer/status\` — verifies container is running 11. \*\*SSH key pair generation\*\* (if not exists): - Algorithm: RSA 4096-bit - Format: PKCS1 PEM (private), OpenSSH (public) - Path: \`~/.ssh/id\_rsa\_{username}\_{hostname}\` and \`.pub\` - Permissions: \`0o600\` (Unix) or \`icacls\` restricted (Windows) 12. \*\*Public key upload\*\*: \`POST /api/v1/user/keys\` → server stores in database 13. \*\*SSH config update\*\*: Writes entry to \`~/.ssh/config\`: \`\`\` Host devstar-remote-orgname-reponame HostName devstar.cn Port 22 User git PreferredAuthentications publickey IdentityFile ~/.ssh/id\_rsa\_alice\_devstar\_cn StrictHostKeyChecking no UserKnownHostsFile /dev/null \`\`\` 14. \*\*ssh-agent\*\*: Runs \`ssh-add ~/.ssh/id\_rsa\_alice\_devstar\_cn\` to load key into agent - Docker CLI uses ssh-agent for authentication (does not read SSH config's IdentityFile) ### Phase 4: Docker Context & Environment (VSCode Plugin) 15. \*\*Save original Docker config\*\* for later restoration: - Current Docker context (\`docker context show\`) - Current \`containers.environment\` from settings.json 16. \*\*Create Docker context\*\*: \`\`\`bash docker context create "devstar-remote-orgname-reponame" \\ --docker "host=ssh://devstar-remote-orgname-reponame" docker context use "devstar-remote-orgname-reponame" \`\`\` 17. \*\*Set \`containers.environment.DOCKER\_HOST\`\*\* in VSCode \`settings.json\`: \`\`\`json { "containers.environment": { "DOCKER\_HOST": "ssh://devstar-remote-orgname-reponame" } } \`\`\` \*\*Why both Docker context AND environment variable?\*\* - Docker context: controls what the Docker CLI connects to - \`containers.environment.DOCKER\_HOST\`: tells the Dev Containers extension to use Docker CLI (via \`dial-stdio\`) instead of trying to SSH into the host for environment detection. Without this, Dev Containers would attempt to open a shell on the SSH host — which Gitea's SSH server does not support. ### Phase 5: Container Attachment (VSCode Plugin → Dev Containers Extension) 18. \*\*Write nameConfig\*\*: Creates \`{containerName}.json\` in Dev Containers' \`nameConfigs/\` directory: \`\`\`json { "workspaceFolder": "/workspace/reponame", "remoteUser": "root" } \`\`\` This tells Dev Containers what folder to open and which user to use when attaching. 19. \*\*Set up port forwarding\*\* (if \`forwardPorts\` specified): - Creates SSH tunnels: \`ssh -N -L {localPort}:localhost:{containerPort}...\` - Each tunnel runs as a detached child process - Tracked for cleanup on extension deactivation 20. \*\*Attach to container\*\*: \`\`\` vscode.commands.executeCommand('remote-containers.attachToRunningContainer', containerName) \`\`\` Dev Containers extension: - Reads \`DOCKER\_HOST=ssh://...\` from \`containers.environment\` - Runs \`docker system dial-stdio\` over SSH to establish API channel - Finds the container by name - Attaches VSCode to the container (installs VS Code Server inside, opens workspace) ### Phase 6: Cleanup (VSCode Plugin) 21. \*\*Deferred restoration\*\* (60 seconds after attachment): - Restores original Docker context - Restores original \`containers.environment\` in settings.json 22. \*\*globalState cleanup\*\*: Clears \`sshUnified\`, \`devstarUsername\`, \`containerName\`, \`workspacePath\` 23. \*\*On error\*\*: Immediately restores Docker config before throwing --- ## 4. SSH Key Lifecycle ### 4.1 Key Generation (Client-Side) \`\`\`mermaid flowchart TD A\["user.ts: createUserSSHKey()"\] --> B\["crypto.generateKeyPairSync('rsa',<br/>modulusLength: 4096)"\] B --> C\["Private Key<br/>PKCS1 PEM format"\] B --> D\["Public Key<br/>OpenSSH format (via sshpk)"\] C --> E\["Write: ~/.ssh/id\_rsa\_{username}\_{hostname}<br/>Permissions: 0o600"\] D --> F\["Write: ~/.ssh/id\_rsa\_{username}\_{hostname}.pub<br/>Permissions: 0o600"\] \`\`\` Key naming convention: \`id\_rsa\_alice\_devstar\_cn\` (dots and colons in hostname replaced with underscores). ### 4.2 Key Upload (Client → Server) \`\`\`mermaid sequenceDiagram participant Plugin as VSCode Plugin participant API as DevStar API participant DB as Server DB participant AK as authorized\_keys participant Containers as Running Dev Containers Plugin->>API: POST /api/v1/user/keys<br/>{ title, key } API->>API: Validate key format API->>DB: Store in public\_key table API->>AK: Rewrite authorized\_keys file API->>Containers: Inject key into ALL running<br/>dev containers of this user API-->>Plugin: 200 OK \`\`\` ### 4.3 Key Injection into Running Containers When a new public key is uploaded, the server calls \`AddPublicKeyToAllRunningDevContainer()\`: \`\`\`go // For each running container owned by this user: docker exec {containerName} sh -c "echo '{publicKey}' >> ~/.ssh/authorized\_keys" \`\`\` This ensures existing containers immediately accept the new key without restart. ### 4.4 Key Usage During Connection \`\`\`mermaid flowchart LR DockerCLI\["Docker CLI<br/>(ssh-agent provides key)"\] SSHServer\["DevStar SSH Server<br/>(checks key against<br/>public\_key table)"\] Serv\["cmd/serv.go<br/>(routes docker commands)"\] DockerCLI -->|SSH| SSHServer --> Serv \`\`\` The Docker CLI connects to \`ssh://devstar-remote-xxx\` using the ssh-agent-loaded key. DevStar's SSH server authenticates the key and routes the Docker command. ### 4.5 Key Storage Locations Summary | Location | What | Who Writes | Who Reads | |----------|------|------------|-----------| | \`~/.ssh/id\_rsa\_{u}\_{h}\` | Private key | Plugin | ssh-agent → Docker CLI | | \`~/.ssh/id\_rsa\_{u}\_{h}.pub\` | Public key | Plugin | Plugin (for upload) | | \`~/.ssh/config\` | SSH host alias | Plugin | Docker CLI (host resolution) | | Server DB \`public\_key\` table | Public key record | Server API | SSH auth | | Server \`{SSH.RootPath}/authorized\_keys\` | All public keys | Server | SSH daemon (sshd/built-in) | | Container \`~/.ssh/authorized\_keys\` | User's public keys | Server (docker exec) | Container's sshd | --- ## 5. Docker-over-SSH Proxy ### 5.1 How It Works When the Docker CLI is configured with \`DOCKER\_HOST=ssh://...\`, it: 1. Opens an SSH connection to the specified host 2. Sends the command \`docker system dial-stdio\` over SSH 3. This establishes a bidirectional byte stream (stdin/stdout) that carries Docker API requests/responses 4. The Docker CLI sends HTTP API calls through this stream, just as it would over a local Unix socket ### 5.2 Server-Side Command Routing \`\`\`mermaid flowchart TD SSH\["SSH Connection"\] SSH --> PK\["modules/ssh/ssh.go<br/>publicKeyHandler() → authenticate key, get keyID<br/>sessionHandler() → spawn 'gitea serv key-{keyID}'"\] PK --> Serv\["cmd/serv.go<br/>Reads SSH\_ORIGINAL\_COMMAND"\] Serv -->|"starts with 'docker'"| Run\["runDockerCommand()"\] Serv -->|"otherwise"| Git\["Standard git command handling"\] Run --> Auth\["1. Authenticate<br/>Verify SSH key maps to valid user"\] Auth --> WL\["2. Whitelist check<br/>ps, inspect, exec, start, stop,<br/>attach, logs, version, info, system"\] WL --> AC\["3. Container access control<br/>containerName must start with<br/>sanitizedUsername + '-'"\] AC --> Exec\["4. Execute<br/>docker {subcommand} {args}<br/>Pipe stdin/stdout/stderr"\] \`\`\` ### 5.3 \`system dial-stdio\` Deep Dive This is the critical command that enables VSCode's Docker-over-SSH: \`\`\`mermaid sequenceDiagram participant VSCode as VSCode<br/>(Docker CLI) participant SSH as SSH Tunnel participant Server as DevStar Server VSCode->>SSH: docker system dial-stdio SSH->>Server: Forward command Server->>Server: exec: docker system dial-stdio<br/>→ connects to /var/run/docker.sock Note over VSCode,Server: Bidirectional Docker API stream established VSCode->>Server: GET /containers/json Server-->>VSCode: Container list VSCode->>Server: POST /containers/.../attach Server-->>VSCode: Container I/O stream \`\`\` The \`dial-stdio\` command opens a raw connection to the Docker daemon socket (\`/var/run/docker.sock\`) and bridges it to SSH's stdin/stdout. This allows the remote Docker CLI to communicate with the daemon as if it were local. --- ## 6. Dev Container Creation & Volume Mounts ### 6.1 Container Creation File: \`services/devcontainer/docker\_agent.go\` When a user creates a dev container, the server: 1. Generates a sanitized container name: \`{username}-{owner}-{repo}\` - Rules: remove non-alphanumeric chars, lowercase, truncate (user: 15, owner: 15, repo: 31) 2. Creates the container with: - \*\*Image\*\*: From \`.devcontainer/devcontainer.json\` or default - \*\*Command\*\*: \`tail -f /dev/null\` (keeps container alive) - \*\*Labels\*\*: - \`devcontainer.local\_folder\`: \`{workspaceDir}/{repoName}\` - \`devcontainer.config\_file\`: path to \`devcontainer.json\` - \*\*Port exposure\*\*: SSH port 22 3. Runs initialization inside the container: - Configures \`/etc/hosts\` (adds \`host.docker.internal\`) - Installs git and SSH server - Clones the repository via HTTP into \`/workspace/{repoName}\` - Generates SSH host keys (\`ssh-keygen -A\`) - Starts SSH service - \*\*Injects all of the user's public keys\*\* into \`~/.ssh/authorized\_keys\` ### 6.2 Volume Mounts | Mount | Host Path | Container Path | Purpose | |-------|-----------|----------------|---------| | \*\*User Workspace\*\* | \`/var/lib/gitea/user-workspace/{username}\` | \`/workspace\` | Persistent workspace data across container rebuilds | | \*\*devcontainer.json Mounts\*\* | User-defined in \`.devcontainer/devcontainer.json\` | User-defined | Project-specific custom mounts | | \*\*Docker Socket (WebTerminal only)\*\* | \`/var/run/docker.sock\` | \`/var/run/docker.sock\` | DooD — allows WebTerminal to manage containers | ### 6.3 DooD (Docker-outside-of-Docker) Path Consideration \*\*Important\*\*: DevStar itself runs inside a Docker container with a named volume: \`\`\`mermaid graph TD Host\["Host OS"\] --> Docker\["Docker Engine"\] Docker --> DevStar\["DevStar Container<br/>(volume: devstar\_data → /var/lib/gitea)"\] Docker --> DevCont\["Dev Container<br/>(/workspace ← HOST's /var/lib/gitea/user-workspace/{user})"\] DevStar -->|"Creates dev containers<br/>via mounted docker.sock"| Docker style DevStar fill:#f9f,stroke:#333 style DevCont fill:#bbf,stroke:#333 \`\`\` The bind mount path in \`-v /var/lib/gitea/user-workspace/alice:/workspace\` resolves from the \*\*host's filesystem\*\*, not from DevStar's container filesystem. This is because \`docker.sock\` talks to the host's Docker daemon directly. --- ## 7. VSCode Plugin Internals ### 7.1 \`firstOpenProject()\` — Entry Point Decision \`\`\`typescript // remote-container.ts, line 89 async firstOpenProject(host, hostname, port, username, path, context) { const sshUnified = context.globalState.get('sshUnified'); // true/false const devstarUsername = context.globalState.get('devstarUsername'); if (sshUnified && devstarUsername) { // ──► Unified Docker-over-SSH path (NEW) const containerName = context.globalState.get('containerName') || this.generateContainerName(devstarUsername, owner, repo); await this.firstConnectUnified(host, hostname, port, username, path, containerName, context); return; } if (vscode.env.remoteName) { // ──► Remote window: delegate to local window via code --open-url (LEGACY)... } else { // ──► Local window: direct SSH connection (LEGACY)... } } \`\`\` ### 7.2 Docker Context Management The plugin creates a \*\*named Docker context\*\* to override Docker Desktop's default \`desktop-linux\` context (which forces connections to the local Docker daemon): \`\`\`bash # Create context pointing to remote Docker via SSH docker context create "devstar-remote-xxx" --docker "host=ssh://devstar-remote-xxx" # Switch to it docker context use "devstar-remote-xxx" \`\`\` After the connection is established (60s delay), the original context is restored: \`\`\`bash docker context use "desktop-linux" # or whatever was original \`\`\` ### 7.3 \`containers.environment.DOCKER\_HOST\` This VSCode setting is written to \`settings.json\` to control how the \*\*Dev Containers extension\*\* connects: \`\`\`json { "containers.environment": { "DOCKER\_HOST": "ssh://devstar-remote-xxx" } } \`\`\` \*\*Why is this needed in addition to Docker context?\*\* When Dev Containers detects an SSH-type Docker context, it tries to SSH into the host and open a \`/bin/sh\` shell to detect the environment (OS, architecture, etc.). DevStar's Gitea SSH server does \*\*not\*\* support shell access — it only supports \`git\` and \`docker\` commands. Setting \`DOCKER\_HOST\` in \`containers.environment\` forces Dev Containers to use Docker CLI commands (which go through \`dial-stdio\`) instead of attempting shell access. This is the key insight that makes the whole architecture work. ### 7.4 \`nameConfigs\` — Workspace Folder Mapping Dev Containers needs to know what folder to open when attaching to a container. This is configured via a JSON file: \`\`\` ~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/nameConfigs/{containerName}.json \`\`\` Content: \`\`\`json { "workspaceFolder": "/workspace/my-repo", "remoteUser": "root" } \`\`\` ### 7.5 Port Forwarding For each port in the \`forwardPorts\` URL parameter, the plugin creates an SSH tunnel: \`\`\`bash ssh -N -L {localPort}:localhost:{containerPort} \\ -p {sshPort} -i {keyPath} \\ -o StrictHostKeyChecking=no \\ root@{hostname} \`\`\` Tunnels are: - Created as detached child processes - Tracked in \`sshTunnelProcesses\[\]\` for cleanup - Killed on extension deactivation (\`dispose()\`) --- ## 8. Security Model ### 8.1 Authentication Chain \`\`\`mermaid flowchart TD Click\["1. access\_token in URL<br/>→ Plugin auto-login to DevStar API<br/>(one-time terminal\_login\_token)"\] Key\["2. RSA 4096-bit key pair<br/>→ SSH authentication<br/>Private key stays on client,<br/>public key uploaded to server"\] SSHAuth\["3. SSH connection authenticated<br/>by Gitea's SSH server<br/>Key verified against public\_key table"\] DockerAuth\["4. Docker commands validated per-user<br/>Container name must match<br/>user's namespace prefix"\] Click --> Key --> SSHAuth --> DockerAuth \`\`\` ### 8.2 Docker Command Whitelist Only these Docker subcommands are allowed through the SSH proxy: | Command | Purpose | |---------|---------| | \`ps\` | List containers | | \`inspect\` | Get container details | | \`exec\` | Execute commands in container | | \`start\` / \`stop\` | Container lifecycle | | \`attach\` | Attach to container (for Dev Containers) | | \`logs\` | View container logs | | \`version\` / \`info\` | Docker daemon info | | \`system\` | Required for \`dial-stdio\` | Commands like \`run\`, \`rm\`, \`build\`, \`pull\`, \`push\` are \*\*not allowed\*\*. ### 8.3 Container Namespace Isolation \`\`\`go // cmd/serv.go — runDockerCommand() sanitizedUsername:= sanitizeUsername(user.Name) // e.g., "alice" if!strings.HasPrefix(containerName, sanitizedUsername + "-") { return "Access denied: You can only access your own containers" } \`\`\` User \`alice\` can only interact with containers named \`alice-\*\`. This prevents cross-user container access even if someone crafts a malicious Docker command. ### 8.4 SSH Key Security - Private key: \`0o600\` permissions (owner read/write only) - Windows: \`icacls\` restricts to current user - \`StrictHostKeyChecking no\` — trusts server identity (acceptable for managed infrastructure) - ssh-agent used for key authentication (key not written to Docker config) --- ## 9. Platform-Specific Considerations ### 9.1 File Path Matrix | Item | macOS | Linux | Windows | WSL | |------|-------|-------|---------|-----| | SSH keys | \`~/.ssh/\` | \`~/.ssh/\` | \`%USERPROFILE%\\.ssh\\\` | \`~/.ssh/\` (WSL home) | | SSH config | \`~/.ssh/config\` | \`~/.ssh/config\` | \`%USERPROFILE%\\.ssh\\config\` | \`~/.ssh/config\` | | VSCode settings | \`~/Library/.../settings.json\` | \`~/.config/Code/.../settings.json\` | \`%APPDATA%\\Code\\...\\settings.json\` | ⚠️ See below | | nameConfigs | \`~/Library/.../nameConfigs/\` | \`~/.config/Code/.../nameConfigs/\` | \`%APPDATA%\\Code\\...\\nameConfigs\\\` | ⚠️ See below | ### 9.2 WSL Known Issues When VSCode is in \*\*WSL Remote\*\* mode, the extension host runs inside WSL, but the Dev Containers extension runs on the \*\*Windows side\*\*: | Problem | Cause | Status | |---------|-------|--------| | \`docker\` CLI not found | Docker Desktop WSL integration not enabled, or \`docker.exe\` not in PATH | Needs fix: fallback to \`docker.exe\` | | \`containers.environment\` write fails | Dev Containers extension schema not visible from WSL extension host | Needs fix: use file-write to Windows-side path | | Settings written to wrong path | \`~/.config/Code/...\` is WSL path; Dev Containers reads from Windows \`%APPDATA%\` | Needs fix: detect WSL and resolve Windows path | | \`dev.containers.executeInWSL\` | Currently forced to \`false\`; should be \`true\` so Docker commands route through WSL where SSH is configured | Needs fix | ### 9.3 Windows-Specific - SSH key permissions set via \`icacls\` instead of \`chmod\` - Terminal detection: PowerShell/CMD detected by shell path containing \`\\\`, \`powershell\`, \`pwsh\`, or \`cmd\` - \`code --open-url\` uses single-quote wrapping for URL: \`'"url"'\` --- ## 10. Sequence Diagram \`\`\`mermaid sequenceDiagram participant Browser participant Server as DevStar Server participant Plugin as VSCode Plugin participant SSHSrv as DevStar SSH Server participant DockerD as Docker Daemon participant DevCont as Dev Container Browser->>Server: Click "Open with VSCode" Server-->>Browser: vscode:// URI with params Browser->>Plugin: Protocol handler activates Note over Plugin: Parse URI & store in globalState Plugin->>Server: Check container status<br/>GET /api/v1/devcontainer Note over Plugin: Generate RSA 4096-bit key pair<br/>(if not exists) Plugin->>Server: Upload public key<br/>POST /api/v1/user/keys Note over Plugin: Write SSH config & ssh-add Note over Plugin: Create Docker context &<br/>set containers.environment Plugin->>SSHSrv: SSH: docker system dial-stdio SSHSrv->>DockerD: Proxy to Docker socket Note over Plugin,DockerD: Bidirectional Docker API stream Plugin->>DevCont: attachToRunningContainer<br/>(via Dev Containers extension) Note over Plugin,DevCont: VSCode Server installed & connected Note over Plugin: Cleanup: restore Docker context<br/>(60s delay) \`\`\` --- ## Appendix: Configuration Reference ### Server-Side Settings (\`app.ini\`) \`\`\`ini \[devcontainer\] SSH\_ENABLED = true; Enable unified SSH entry SSH\_PORT = 22; SSH port for Docker-over-SSH USER\_WORKSPACE\_BASE\_PATH = /var/lib/gitea/user-workspace; Host path for workspace volumes CONTAINER\_WORKSPACE\_DIR = /workspace; Container-side workspace mount point \`\`\` ### IDE URL Template (\`modules/setting/config.go\`) \`\`\` vscode://mengning.devstar/openProject? host={host}&hostname={hostname}&port={port}&username={username}&path={path} &access\_token={token}&devstar\_username={devstar\_username}&devstar\_domain={domain} &sshUnified={sshUnified}&containerName={containerName}&workspacePath={workspacePath} \`\`\` ### Container Naming Convention \`\`\` Format: {sanitized\_username}-{sanitized\_owner}-{sanitized\_repo} Rules: \[^a-zA-Z0-9\] removed, lowercased Limits: username(15) - owner(15) - repo(31) Example: alice-myorg-myproject \`\`\` Both server (\`getSanitizedDevcontainerName\`) and plugin (\`generateContainerName\`) use identical logic to ensure the container name matches.

👍 1

**3 名参与者**

**通知**

**时间跟踪**

**截止日期**

未设置截止日期。

**依赖工单**  

未设置依赖工单。

引用：devstar/devstar#108