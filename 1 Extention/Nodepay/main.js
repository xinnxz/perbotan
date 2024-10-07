import fs from 'fs';
import fetch from 'node-fetch';
import { v4 as uuidv4 } from 'uuid';
import log4js from 'log4js';
import { HttpsProxyAgent } from 'https-proxy-agent';

const logger = log4js.getLogger();
logger.level = 'info'; // 로깅 레벨 설정

// 상수
const NP_TOKEN = process.env.nptoken; // 환경변수에서 nptoken을 가져옴
const PING_INTERVAL = 30000; // 30초
const RETRIES_LIMIT = 60; // 핑 실패에 대한 전역 재시도 한도

const DOMAIN_API = {
  SESSION: "https://api.nodepay.ai/api/auth/session", // 세션 API
  PING: "https://nw2.nodepay.ai/api/network/ping" // 핑 API
};

const CONNECTION_STATES = {
  CONNECTED: 1, // 연결됨
  DISCONNECTED: 2, // 연결 끊김
  NONE_CONNECTION: 3 // 연결 없음
};

let statusConnect = CONNECTION_STATES.NONE_CONNECTION; // 연결 상태 초기화
let tokenInfo = NP_TOKEN;
let browserId = null;
let accountInfo = {};

// 파일에서 프록시를 로드하는 함수
function loadProxies(proxyFile) {
  try {
    const proxies = fs.readFileSync(proxyFile, 'utf-8').split('\n').filter(Boolean);
    return proxies;
  } catch (err) {
    logger.error(`프록시 파일 ${proxyFile}을 읽는 도중 오류가 발생했습니다: ${err.message}`);
    return [];
  }
}

// 응답을 검증하는 함수
function validResp(resp) {
  if (!resp || resp.code < 0) {
    throw new Error("잘못된 응답입니다");
  }
  return resp;
}

// 프로필 정보를 렌더링하는 함수
async function renderProfileInfo(proxy) {
  try {
    const npSessionInfo = loadSessionInfo(proxy);

    if (!npSessionInfo) {
      const response = await callApi(DOMAIN_API.SESSION, {}, proxy);
      validResp(response);
      accountInfo = response.data;
      if (accountInfo.uid) {
        saveSessionInfo(proxy, accountInfo);
        await startPing(proxy);
      } else {
        handleLogout(proxy);
      }
    } else {
      accountInfo = npSessionInfo;
      await startPing(proxy);
    }
  } catch (error) {
    logger.error(`프록시 ${proxy}에 대한 renderProfileInfo에서 오류 발생: ${error.message}`);
    if (error.message.includes("500 Internal Server Error")) {
      logger.info(`오류가 발생한 프록시 목록에서 제거: ${proxy}`);
      removeProxyFromList(proxy);
      return null;
    } else {
      logger.error(`연결 오류: ${error.message}`);
      return proxy;
    }
  }
}

// API 호출을 수행하는 함수
async function callApi(url, data, proxy) {
  const headers = {
    "Authorization": `Bearer ${tokenInfo}`,
    "Content-Type": "application/json"
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(data),
      agent: proxy ? new HttpsProxyAgent(proxy) : null
    });

    if (!response.ok) {
      throw new Error(`${url}로의 API 호출 실패`);
    }

    const jsonResponse = await response.json();
    return validResp(jsonResponse);
  } catch (error) {
    logger.error(`API 호출 중 오류 발생: ${error.message}`);
    throw error;
  }
}

// 핑을 시작하는 함수
async function startPing(proxy) {
  try {
    await ping(proxy);
    setInterval(async () => {
      await ping(proxy);
    }, PING_INTERVAL);
  } catch (error) {
    logger.error(`프록시 ${proxy}에 대한 startPing에서 오류 발생: ${error.message}`);
  }
}

// 핑을 수행하는 함수
async function ping(proxy) {
  let retries = 0;

  try {
    const data = {
      id: accountInfo.uid,
      browser_id: browserId,
      timestamp: Math.floor(Date.now() / 1000)
    };

    const response = await callApi(DOMAIN_API.PING, data, proxy);
    if (response.code === 0) {
      logger.info(`프록시 ${proxy}를 통한 핑 성공`);
      retries = 0;
      statusConnect = CONNECTION_STATES.CONNECTED;
    } else {
      handlePingFail(proxy, response);
    }
  } catch (error) {
    logger.error(`프록시 ${proxy}를 통한 핑 실패: ${error.message}`);
    handlePingFail(proxy, null);
  }
}

// 핑 실패를 처리하는 함수
function handlePingFail(proxy, response) {
  if (response && response.code === 403) {
    handleLogout(proxy);
  } else {
    statusConnect = CONNECTION_STATES.DISCONNECTED;
  }
}

// 로그아웃을 처리하는 함수
function handleLogout(proxy) {
  tokenInfo = null;
  statusConnect = CONNECTION_STATES.NONE_CONNECTION;
  accountInfo = {};
  saveSessionInfo(proxy, null);
  logger.info(`프록시 ${proxy}에 대해 로그아웃하고 세션 정보를 초기화했습니다.`);
}

// 세션 정보를 로드하는 함수
function loadSessionInfo(proxy) {
  // 세션 로드 구현
  return {};
}

// 세션 정보를 저장하는 함수
function saveSessionInfo(proxy, data) {
  // 세션 저장 구현
}

// 프록시가 유효한지 확인하는 함수
function isValidProxy(proxy) {
  // 프록시 유효성 검사
  return true;
}

// 프록시를 목록에서 제거하는 함수
function removeProxyFromList(proxy) {
  // 프록시 제거 구현
}

// 메인 함수
async function main() {
  const allProxies = loadProxies('proxy.txt');
  let activeProxies = allProxies.slice(0, 100).filter(isValidProxy);

  const tasks = new Map();
  for (const proxy of activeProxies) {
    tasks.set(renderProfileInfo(proxy), proxy);
  }

  while (true) {
    const doneTasks = await Promise.allSettled(Array.from(tasks.keys())); // 모든 작업이 완료될 때까지 대기
    for (const doneTask of doneTasks) {
      const failedProxy = tasks.get(doneTask);

      if (doneTask.status === 'rejected') {
        logger.info(`실패한 프록시 제거 및 교체: ${failedProxy}`);
        activeProxies = activeProxies.filter(p => p !== failedProxy);
        const newProxy = allProxies.shift();
        if (newProxy && isValidProxy(newProxy)) {
          activeProxies.push(newProxy);
          tasks.set(renderProfileInfo(newProxy), newProxy);
        }
      }

      tasks.delete(doneTask); // 작업 완료 후 제거
    }

    await new Promise(resolve => setTimeout(resolve, 3000)); // 다음 작업 전 3초 대기
  }
}

// SIGINT(Ctrl+C) 처리
process.on('SIGINT', () => {
  logger.info("사용자에 의해 프로그램이 종료되었습니다.");
  process.exit();
});

// 메인 함수 호출
main();
