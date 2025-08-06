FROM debian:bookworm-slim AS builder
ARG USERNAME=vscode
ARG GROUPNAME=vscode
ARG UID=1000
ARG GID=1000
RUN : \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates=* curl=* unzip=* xz-utils=* \
    && groupadd -g $GID $GROUPNAME \
    && useradd -l -m -s /bin/bash -u $UID -g $GID $USERNAME
WORKDIR /opt
SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]
ADD https://dprint.dev/install.sh dprint-installer.sh
ADD https://get.volta.sh volta-installer.sh
ADD https://astral.sh/uv/install.sh uv-installer.sh
RUN : \
    && touch volta-completions node-completions npm-completions uv-completions \
    && chown $USERNAME:$GROUPNAME ./*-completions \
    && chmod +r ./*-installer.sh
USER $USERNAME
RUN : \
    && bash dprint-installer.sh \
    && bash volta-installer.sh \
    && bash uv-installer.sh \
    && /home/$USERNAME/.volta/bin/volta install node \
    && /home/$USERNAME/.volta/bin/npm install -g @biomejs/biome vite@latest markuplint@latest \
    && /home/$USERNAME/.local/bin/uv tool install ruff@latest \
    && /home/$USERNAME/.local/bin/uv tool install ty@latest \
    && /home/$USERNAME/.local/bin/uv tool install shellcheck-py@latest \
    && /home/$USERNAME/.local/bin/uv tool install shfmt-py@latest \
    && /home/$USERNAME/.volta/bin/volta completions bash > volta-completions \
    && /home/$USERNAME/.volta/bin/node --completion-bash > node-completions \
    && /home/$USERNAME/.volta/bin/npm completion > npm-completions \
    && /home/$USERNAME/.local/bin/uv generate-shell-completion bash > uv-completions \
    && echo "alias ll='ls -lha --color=auto'" >> ~/.bash_aliases \
    && echo "alias ..='cd ..'" >> ~/.bash_aliases

FROM mcr.microsoft.com/vscode/devcontainers/base:bookworm
ARG USERNAME=vscode
ARG GROUPNAME=vscode
ENV PYTHONUNBUFFERED=True
ENV UV_LINK_MODE=copy
COPY --from=builder /opt/*-completions /etc/bash_completion.d/
COPY --from=builder /home/$USERNAME/.bash_aliases /home/$USERNAME/
COPY --from=builder /home/$USERNAME/.dprint /home/$USERNAME/.dprint
COPY --from=builder /home/$USERNAME/.volta /home/$USERNAME/.volta
COPY --from=builder /home/$USERNAME/.local/bin/uv* /home/$USERNAME/.local/bin/
COPY --from=builder /home/$USERNAME/.local/bin/ruff /home/$USERNAME/.local/bin/
COPY --from=builder /home/$USERNAME/.local/bin/ty /home/$USERNAME/.local/bin/
COPY --from=builder /home/$USERNAME/.local/bin/shellcheck /home/$USERNAME/.local/bin/
COPY --from=builder /home/$USERNAME/.local/bin/shfmt /home/$USERNAME/.local/bin/
RUN chown -R $USERNAME:$GROUPNAME /home/$USERNAME
USER $USERNAME
# hadolint ignore=SC2016
RUN : \
    && /home/$USERNAME/.local/bin/uv tool install pre-commit@latest \
    && echo '[ -d "$HOME/.dprint/bin" ] && PATH="$HOME/.dprint/bin:$PATH"' >> /home/$USERNAME/.profile \
    && echo '[ -d "$HOME/.volta/bin" ] && PATH="$HOME/.volta/bin:$PATH"' >> /home/$USERNAME/.profile
