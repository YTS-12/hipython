USE WNTRADE;
/*
  * 테이블 개수 1개 -> 심플 쿼리
  * 테이블 2개 이상 -> 조인
  * 크로스 조인(카테지안 프로덕트 연산) m개 * n개 결과를 반환
  * 내부조인 (이너조인) -> 조건에 만족하는 데이터만 반환 - 동등조인, 비동등조인
*/

SELECT 부서.부서번호
	  ,사원.부서번호
	  ,부서명
      ,이름
FROM 부서
CROSS JOIN 사원
ON 부서.부서번호 = 사원.부서번호
WHERE 이름 = '배재용';

SELECT 주문번호
      ,고객회사명
      ,주문일
FROM 주문
JOIN 고객
ON 주문.고객번호 = 고객.고객번호
WHERE 주문.고객번호 = 'ITCWH';

SELECT 주문번호
	  ,주문.사원번호
      ,고객번호
      ,사원.이름
	  
FROM 주문
JOIN 사원
ON 주문.사원번호 = 사원.사원번호;

SELECT 고객회사명, 제품명
FROM 고객
JOIN 제품;

SELECT 고객회사명
	  ,고객.마일리지
      ,마일리지등급.등급명
FROM 고객
JOIN 마일리지등급
ON 고객.마일리지 BETWEEN 마일리지등급.하한마일리지 AND 마일리지등급.상한마일리지;

USE WNTRADE;
-- 비동등 조인 --
SELECT 주문번호
	  ,이름 AS 사원명
      ,입사일
      ,주문일
FROM 주문
JOIN 사원
ON 주문.사원번호 = 사원.사원번호
AND 주문.주문일 >= 사원.입사일;

-- 고객회사들이 주문한 건수 집계 > 건수가 많은 순서로 출력
SELECT
    고객.고객회사명,
    COUNT(*) AS 주문건수
FROM 고객
JOIN 주문
  ON 주문.고객번호 = 고객.고객번호
GROUP BY 고객.고객회사명
ORDER BY COUNT(*) DESC;

SELECT
    고객.고객회사명,
    고객.담당자명,
    주문.주문일,
    SUM(주문세부.단가 * 주문세부.주문수량) AS 주문금액
FROM 고객
JOIN 주문
  ON 고객.고객번호 = 주문.고객번호
JOIN 주문세부
  ON 주문세부.주문번호 = 주문.주문번호
GROUP BY 고객.고객회사명, 고객.담당자명, 주문.주문일
ORDER BY 주문금액 DESC;


-- 외부조인 --
SELECT 사원번호, 이름, 부서명
FROM 사원
LEFT JOIN 부서
ON 사원.부서번호 = 부서.부서번호;


SELECT
    부서.부서명,
    부서.부서번호,
    사원.이름
FROM 부서
LEFT JOIN 사원
  ON 사원.부서번호 = 부서.부서번호
WHERE 이름 IS NULL;
  
  
SELECT
    고객.고객번호,
    고객.고객회사명,
    주문.주문번호
FROM 고객
LEFT JOIN 주문
  ON 주문.고객번호 = 고객.고객번호
WHERE 주문.주문번호 IS NULL;




