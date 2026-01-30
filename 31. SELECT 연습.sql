SELECT 고객번호, 고객회사명 
FROM 고객
WHERE 마일리지 >= 100
ORDER BY 마일리지 ASC
LIMIT 10;
SELECT 고객번호, 
	   담당자명, 
	   고객회사명 AS 이름, 
       마일리지 AS 포인트, 
       마일리지*1.1 AS "10%인상된 마일리지"
       FROM 고객
	   WHERE 도시 = '서울특별시'
       ORDER BY 마일리지 DESC
       LIMIT 20;
SELECT 이름 AS 직원명
	   ,주소
       ,직위 
       FROM 사원;
SELECT
  제품명,
  FORMAT(단가, 0) AS 단가,
  재고 AS 구매가능수량,
  FORMAT(재고 * 단가, 0) AS 주문가능금액
FROM 제품
ORDER BY 재고 ASC
LIMIT 20;
SELECT 제품번호
	,FORMAT (단가, 0) AS 단가
	,주문수량
	,FORMAT (단가*주문수량, 0) AS 주문금액
	,할인율
    ,FORMAT(단가*주문수량*할인율, 0) AS 할인금액
	,FORMAT(단가*주문수량*(1-할인율), 0) AS 최종주문금액 
    FROM 주문세부
	LIMIT 20;
SELECT 고객번호
	   ,담당자명
       ,마일리지
FROM 고객
WHERE 마일리지 >= 100000;

SELECT 제품번호
	   ,제품명
       ,재고
FROM 제품
WHERE 단가 >= 10000
ORDER BY 단가 DESC;

SELECT 제품명
       ,단가
       ,재고
FROM 제품
WHERE 단가*재고 >= 100000
ORDER BY 재고 ASC
LIMIT 10;

SELECT 이름
	   ,입사일
FROM 사원
WHERE 직위 = '사원'
ORDER BY 이름 ASC;

SELECT 고객번호
	   ,담당자명
       ,도시
       ,마일리지 AS 포인트
FROM 고객
WHERE 도시 = '서울특별시'
ORDER BY 마일리지 DESC
LIMIT 20;

SELECT DISTINCT 도시
FROM 고객;

SELECT 23+5 AS 더하기
	  ,23-5 AS 빼기
      ,23*5 AS 곱하기
      ,23/5 AS 실수나누기
      ,23 DIV 5 AS 정수나누기
      ,23%5 AS 나머지1
      ,23 MOD 5 AS 나머지2;

SELECT 23 >= 5
	  ,23 <= 5
      ,23 < 23
      ,23 > 23
      ,23 = 23
      ,23 != 23
      ,23 <> 23;
      
SELECT*
FROM 고객
WHERE 담당자직위 != '대표 이사';

SELECT*
FROM 주문
WHERE 주문일 < '2021-01-01';

DESCRIBE 주문;

SELECT*
FROM 고객
WHERE 도시 = '부산광역시'
AND 마일리지 < 1000;

SELECT*
FROM 고객
WHERE 도시 = '서울특별시'
AND 마일리지 >= 5000;

SELECT*
FROM 고객
WHERE 도시 = '서울특별시'
OR 마일리지 >= 10000;

SELECT*
FROM 고객
WHERE 도시 != '서울특별시';

SELECT*
FROM 고객
WHERE 도시 != '서울특별시'
AND 마일리지 >= 5000;

SELECT*
FROM 고객
WHERE 도시 = '서울특별시'
OR 도시 = '부산광역시';

SELECT 고객번호
	  ,담당자명
      ,마일리지
      ,도시
FROM 고객
WHERE 도시 = '부산광역시'
UNION
SELECT 고객번호
	  ,담당자명
      ,마일리지
      ,도시
FROM 고객
WHERE 마일리지 < 1000
ORDER BY 1;

SELECT 고객번호
	  ,담당자명
      ,마일리지
      ,도시
FROM 고객
WHERE 도시 = '부산광역시'
OR 마일리지 < 1000
ORDER BY 1;

SELECT 고객번호
	  ,담당자명
      ,마일리지
      ,도시
FROM 고객
WHERE 도시 = '부산광역시'
UNION ALL
SELECT 고객번호
	  ,담당자명
      ,마일리지
      ,도시
FROM 고객
WHERE 마일리지 < 1000
ORDER BY 1;

SELECT*
FROM 주문세부
WHERE 할인율 >= 0.5
OR 단가 >= 5000
ORDER BY 단가;

SELECT 도시
FROM 사원
UNION
SELECT 도시
FROM 고객;

SELECT*
FROM 고객
WHERE 지역 = '';

SELECT*
FROM 고객
ORDER BY 지역 = ''DESC, 도시;

SELECT 고객번호
	  ,담당자명
      ,담당자직위
FROM 고객
WHERE 담당자직위 IN ('영업과장', '마케팅 과장');

SELECT 사원번호
	  ,이름
      ,직위
      ,부서번호
FROM 사원
WHERE 부서번호 IN ('A1', 'A2')
ORDER BY 부서번호;

SELECT 주문번호
	  ,주문일
FROM 주문
WHERE 주문일 BETWEEN '2020-06-01' AND '2020-06-11';

SELECT *
FROM 고객
WHERE 담당자명 BETWEEN '권기호' AND '김도현'
ORDER BY 담당자명;

/* 쿼리 실행순서
* FROM
* WHERE
* SELECT
* ORDER BY
* LIMIT
*/
/* SQL 작성규칙
* 대소문가 구분 없음 -> 명령어, 테이블명, 컬럼명. 단, 컬람값 제외
* 여러줄에 걸쳐 작성 -> 마지막에 ; 필수 '들여쓰기'
* 명령어는 대문자로 쓰는게 일반적이다.
* 컬럼목록, 테이블 목록은 (콤마)로 연결한다. 순서중요
*/

USE WNTRADE;
SELECT*
FROM 고객
WHERE 고객번호 LIKE 'C%';

SELECT*
FROM 고객
WHERE 고객번호 LIKE '__C%';

SELECT*
FROM 고객
WHERE 고객번호 LIKE '%C';

SELECT*
FROM 고객
WHERE (도시 LIKE '%광역시')
AND (고객번호 LIKE '_C%' OR 고객번호 LIKE '__C%');

