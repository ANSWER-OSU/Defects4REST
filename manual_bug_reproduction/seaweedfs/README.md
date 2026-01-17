### Prerequisites

Install **Go 1.22.x** (required for SeaweedFS):

```bash
cd /tmp
wget https://go.dev/dl/go1.22.6.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.6.linux-amd64.tar.gz
```

Add Go to your PATH for the current shell:

```bash
export PATH=$PATH:/usr/local/go/bin
```

(Optional) persist PATH:

```bash
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
```

Verify installation:

```bash
go version
```
