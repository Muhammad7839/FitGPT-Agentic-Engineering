FROM node:22-slim AS node-runtime

FROM python:3.12-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    curl \
    git \
    bash \
    ca-certificates \
    nano \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node-runtime /usr/local/bin/node /usr/local/bin/node
COPY --from=node-runtime /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

COPY .agentic/container/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the Target Codebase backend dependencies used by its existing tests.
COPY backend/requirements.txt /tmp/fitgpt-backend-requirements.txt
RUN python -m pip install --no-cache-dir \
    --requirement /tmp/fitgpt-backend-requirements.txt \
    && rm -f /tmp/fitgpt-backend-requirements.txt

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code@2.1.220

# Install OpenCode
RUN npm install -g opencode-ai@1.18.10

# Install ngrok
RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | tee /etc/apt/sources.list.d/ngrok.list \
    && apt-get update && apt-get install -y ngrok \
    && rm -rf /var/lib/apt/lists/*

# Claude Code configuration: default settings + status line
RUN mkdir -p /root/.claude
COPY .agentic/container/settings.json /root/.claude/settings.json
COPY .agentic/container/statusline.sh /root/.claude/statusline.sh
RUN chmod +x /root/.claude/statusline.sh

# Copy entrypoint script
COPY .agentic/container/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Student shell quality-of-life improvements
RUN echo 'export PS1="ai-course:\\w# "' >> /root/.bashrc && \
    echo 'alias ll="ls -alF"' >> /root/.bashrc && \
    echo 'alias la="ls -A"' >> /root/.bashrc && \
    echo 'alias l="ls -CF"' >> /root/.bashrc && \
    echo 'alias python="python3"' >> /root/.bashrc && \
    echo 'alias pip="pip3"' >> /root/.bashrc

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]
