# 1. Node.js v20 이미지 사용
FROM node:20

# 2. 컨테이너 내 작업 디렉토리 설정 (web/my-app으로 설정)
WORKDIR /usr/src/app

# 3. package.json 및 package-lock.json 복사
COPY package*.json ./

# 4. 의존성 설치
RUN npm install

# 5. 프로젝트 전체 복사
COPY . .

# 6. React 개발 서버 실행
CMD ["npm", "start"]

# 7. React 개발 서버 포트 노출
EXPOSE 3000
