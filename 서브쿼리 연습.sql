use wntrade;
SELECT  A.고객회사명, A.담당자명, A.마일리지
FROM 고객 A
LEFT JOIN 고객 B
ON A.마일리지 < B.마일리지
WHERE B.고객번호 IS NULL;

SELECT 고객번호
      ,고객회사명
      ,담당자명
      ,마일리지
      ,등급명
FROM 고객
JOIN 마일리지등급
ON 마일리지 >= 하한마일리지
AND 마일리지 <= 상한마일리지;

SELECT 사원번호
      ,이름
      ,부서명
FROM 사원
LEFT JOIN 부서
ON 사원.부서번호 = 부서.부서번호;

SELECT 부서명
	  ,사원.*
FROM 사원
RIGHT JOIN 부서
ON 사원.부서번호 = 부서.부서번호
WHERE 사원.부서번호 IS NULL;


SELECT 이름
      ,부서.*
FROM 사원
LEFT JOIN 부서
ON 사원.부서번호 = 부서.부서번호
WHERE 부서.부서번호 IS NULL;


SELECT 고객.*
FROM 고객
LEFT JOIN 주문
ON 고객.고객번호 = 주문.고객번호
WHERE 주문.주문상사번호번호 IS NULL;

SELECT 사원.이름, 사원.사원번호, 상사.이름, 상사.사원번호
FROM 사원 JOIN 사원 AS 상사
ON 사원.상사번호 = 상사.사원번호;

SELECT 고객번호
      ,고객회사명
      ,담당자명
      ,마일리지
FROM 고객
WHERE 마일리지 = (SELECT MAX(마일리지) FROM 고객);

SELECT 고객회사명
      ,담당자명
FROM 고객
JOIN 주문
ON 고객.고객번호 = 주문.고객번호
WHERE 주문번호 = 'H0250';


SELECT 담당자명
      ,고객회사명
      ,마일리지
FROM 고객
WHERE 마일리지 > ANY (SELECT 마일리지 
					FROM 고객 
					WHERE 도시 = '부산광역시');

SELECT 담당자명
      ,고객회사명
      ,마일리지
FROM 고객
WHERE 마일리지 > ALL (SELECT AVG(마일리지)
					FROM 고객
                    GROUP BY 지역);

SELECT 고객번호
	  ,고객회사명
FROM 고객
WHERE EXISTS (SELECT *
             FROM 주문 
             WHERE 고객번호 = 고객.고객번호);

SELECT 도시
	  ,AVG(마일리지) AS 평균마일리지
FROM 고객
group by 도시
HAVING AVG(마일리지) > (SELECT AVG(마일리지) FROM 고객);

SELECT 담당자명
	  ,고객회사명
      ,마일리지
      ,고객.도시
      ,도시_평균마일리지
      ,(도시_평균마일리지 - 마일리지) AS 차이
FROM 고객
	,(SELECT 도시 ,AVG(마일리지) AS 도시_평균마일리지
    FROM 고객
    GROUP BY 도시) AS 도시별요약
WHERE 고객.도시 = 도시별요약.도시;

SELECT 고객번호
      ,담당자명
      ,(SELECT MAX(주문일)
		FROM 주문
        WHERE 주문.고객번호 = 고객.고객번호) AS 최종주문일
FROM 고객;