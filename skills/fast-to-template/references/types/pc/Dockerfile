FROM image-docker.zuoyebang.cc/base/node-builder:20-slim AS builder

WORKDIR /home/homework/

ARG CI_FE_DEBUG
ARG APP_NAME
ENV APP_NAME ${APP_NAME}

COPY package.json bun.lockb ./
RUN npm config set registry http://ued.zuoyebang.cc/npm/ && \
    npm install -g bun && \
    bun install --frozen-lockfile

COPY . .

RUN if [ "$CI_FE_DEBUG" = "true" ]; then \
    bun run build:test; \
    else \
    bun run build:prod; \
    fi

FROM image-docker.zuoyebang.cc/privbase/fe-nginx:1.2.9

ARG APP_NAME
ENV APP_NAME $APP_NAME
ARG REPO_NAME
ENV REPO_NAME $REPO_NAME

COPY --from=builder /home/homework/dist/ /home/homework/www/static/$APP_NAME/

CMD ["nginx", "-g", "daemon off;"]
