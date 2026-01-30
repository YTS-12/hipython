use WNTRADE;

-- 단일행 함수
-- 1. 문자함수
-- 2. 숫자함수
-- 3. 날짜함수
-- 집계함수


select FIELD('SQL', 'SQL', 'JAVA', 'C');

select FIELD('오땅', '홈런볼', '오땅', '초콜릿'); #2

select REPLACE('ABC-DEF', '-', '*');

select REVERSE('ABCDEF');

select NOW(), SYSDATE(); -- 현재 날짜시간
select CURDATE(), CURTIME();

select NOW() as 'START', SLEEP(5), NOW() as 'END'; -- 시작시간 기준
select SYSDATE() as 'START',SLEEP(5),  SYSDATE() as 'END';  -- 호출시간 기준


SELECT IF(12500*450 > 5000000, '초과달성', '미달성');

SELECT 고객번호, IF(마일리지 >= 1000, 'VIP', '일반등급') AS 등급
FROM 고객;

SELECT 사원번호, 이름, IF(도시 = "서울특별시", "수도권", "지방")
FROM 사원;

SELECT CASE WHEN 12500*450 > 5000000 THEN '초과달성'
		    WHEN 2500*450 > 4000000 THEN '달성'
            ELSE '미달성'
		END;
	
SELECT 주문번호
      ,단가
      ,주문수량 
      ,CASE
			WHEN 단가*주문수량 >= 5000000 THEN '초과달성'
			WHEN 단가*주문수량 <= 4000000 THEN '달성'
			ELSE '미달성'
END AS 달성여부
FROM 주문세부;

SELECT 고객번호,
       마일리지,
       CASE
         WHEN 마일리지 > 50000 THEN 'VIP'
         WHEN 마일리지 > 10000 THEN 'GOLD'
         WHEN 마일리지 > 5000  THEN 'SILVER'
         ELSE 'BRONZE'
       END AS `마일리지 등급`
FROM 고객;

SELECT 사원번호, 이름, 부서번호,
  CASE 부서번호
    WHEN '10' THEN '영업부'
    WHEN '20' THEN '총무부'
    WHEN '30' THEN 'IT개발부'
    ELSE '기타부서'
  END AS 부서명_가상
FROM 사원;

SELECT
    주문번호,
    주문일,
    요청일,
    발송일,
    CASE
        WHEN 발송일 IS NULL THEN '배송대기'
        WHEN 요청일 IS NOT NULL AND 발송일 <= 요청일 THEN '빠른배송'
        ELSE '일반배송'
    END AS 배송상태
FROM 주문;

SELECT
    고객번호,
    고객회사명,
    CONCAT('**', SUBSTRING(고객회사명, 3)) AS 고객회사명_마스킹
FROM 고객;

SELECT
    FLOOR(단가 * 주문수량) AS 주문금액,
    FLOOR(단가 * 주문수량 * 할인율) AS 할인금액,
    FLOOR(단가 * 주문수량 * (1 - 할인율)) AS 실제주문금액
FROM 주문세부;

SELECT COUNT(*)
	  ,COUNT(고객번호)
      ,COUNT(도시)
      ,COUNT(DISTINCT 지역)
      ,SUM(마일리지)
      ,AVG(마일리지)
      ,MIN(마일리지)
      FROM 고객
      -- WHERE 도시 LIKE '서울%'
      GROUP BY 도시;

SELECT 담당자직위
      ,도시
	  ,COUNT(고객번호)
      ,SUM(마일리지)
      ,AVG(마일리지)
      FROM 고객
      group by 담당자직위, 도시;
      
SELECT 도시
	  ,count(고객번호)
      ,avg(마일리지)
FROM 고객
GROUP BY 도시
HAVING avg(마일리지) >= 1000;

SELECT 도시
	  ,SUM(마일리지)
FROM 고객
WHERE 고객번호 LIKE 'T%'
GROUP BY 도시
HAVING SUM(마일리지) >= 1000;

SELECT 담당자직위
	  ,MAX(마일리지)
      ,SUM(마일리지)
FROM 고객
WHERE 도시 LIKE '%광역시'
GROUP BY 담당자직위
WITH ROLLUP  -- 총계 행이 추가된다.
HAVING SUM(마일리지) >= 10000;

SELECT 도시
      ,COUNT(*) AS 고객수
      ,AVG(마일리지) AS 평균마일리지
FROM 고객
GROUP BY 도시
WITH ROLLUP;