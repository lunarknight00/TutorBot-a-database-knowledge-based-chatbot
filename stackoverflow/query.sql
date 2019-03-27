-- Qeury on https://data.stackexchange.com/stackoverflow/query/new
-- Most 10000 Upvoted Answers of sql related questions
-- The most Upvoted qAnswers of All Time on SO

select top 10000 count(v.postid) as 'Vote count',p.title,p.body
from votes v join posts p  on p.id=v.postid 
where p.PostTypeId = 1 and p.Tags like ('%sql%')
group by v.postid,p.body,p.Tags,p.title
order by 'Vote count' desc


--- basic query

SELECT TagName, QuestionID AS [Post Link],Questions, q_.Score AS [Q score],Answers,
  AnswerID AS [Post Link], a_.Score AS [A score]
FROM
(SELECT TagName,
  (SELECT TOP 1 q.Id
     FROM Posts AS q INNER JOIN PostTags AS qt ON q.Id = qt.PostId
     WHERE qt.TagId = t.Id ORDER BY q.Score DESC) AS QuestionID,
  (SELECT TOP 1 a.Id
     FROM Posts AS a INNER JOIN PostTags AS at ON a.ParentId = at.PostId
     WHERE at.TagId = t.Id ORDER BY a.Score DESC) AS AnswerID,
   (SELECT TOP 1 a.body
     FROM Posts AS a INNER JOIN PostTags AS at ON a.ParentId = at.PostId
     WHERE at.TagId = t.Id ORDER BY a.Score DESC) AS Answers,
    (SELECT TOP 1 q.body
     FROM Posts AS q INNER JOIN PostTags AS qt ON q.Id = qt.PostId
     WHERE qt.TagId = t.Id ORDER BY q.Score DESC) AS Questions
  FROM Tags AS t
  WHERE t.TagName LIKE 'sql%') AS temp
  INNER JOIN Posts AS q_ ON temp.QuestionId = q_.Id
  LEFT OUTER JOIN Posts AS a_ ON temp.AnswerId = a_.Id
  ORDER BY q_.Score DESC

--- sql

SELECT Questions,Answers
FROM
(SELECT TagName,
  (SELECT TOP 1 q.Id
     FROM Posts AS q INNER JOIN PostTags AS qt ON q.Id = qt.PostId
     WHERE qt.TagId = t.Id ORDER BY q.Score DESC) AS QuestionID,
  (SELECT TOP 1 a.Id
     FROM Posts AS a INNER JOIN PostTags AS at ON a.ParentId = at.PostId
     WHERE at.TagId = t.Id ORDER BY a.Score DESC) AS AnswerID,
   (SELECT TOP 1 a.body
     FROM Posts AS a INNER JOIN PostTags AS at ON a.ParentId = at.PostId
     WHERE at.TagId = t.Id ORDER BY a.Score DESC) AS Answers,
    (SELECT TOP 1 q.body
     FROM Posts AS q INNER JOIN PostTags AS qt ON q.Id = qt.PostId
     WHERE qt.TagId = t.Id ORDER BY q.Score DESC) AS Questions
  FROM Tags AS t
  WHERE t.TagName LIKE '%sql%') AS temp
  INNER JOIN Posts AS q_ ON temp.QuestionId = q_.Id
  LEFT OUTER JOIN Posts AS a_ ON temp.AnswerId = a_.Id
  ORDER BY q_.Score DESC
