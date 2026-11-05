# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The White Calzone
- Step 0.12, results of the three runs without a session (optional):
  - Runs without a session: 3
  - Successful logins: 0
  - Failed logins: 3
  - Result: all 3 login attempts returned 401.
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, or 3 tools

## Defect report
- Title: Excluding all cutting tools causes an internal server error
- Request: `POST /api/pizza` with `{"excludedTools":["Knife","Pizza cutter","Scissors"]}` and a valid user token.
- Expected result: HTTP 400 with a JSON error explaining that no pizza can satisfy the request.
- Actual result: HTTP 500 with an empty response body.
- Severity: Medium; a valid but unsatisfiable request produces an unhandled server error instead of a client error.

## Part A
- Step A4, status codes when the other user reads, changes and deletes: 404, 400, 400

## Part B
1. API tests can find integration failures, such as a request reaching the wrong server or a cookie not being retained, and mismatches between the deployed server's actual response and its contract. Unit tests with stubs replace those parts, so they cannot find such failures. Unit tests are still useful because they are faster, isolate the faulty logic, and run without an internet connection.
2. A fresh user and its own records keep tests independent and prevent changes to shared ratings or interference from another student's data. In Project 2, I will make a unique test account for each test and only create, change, or delete shop or hotel data that the test itself created.
3. One `requests.Session` keeps the load-balancer cookies, so the user's create, login, and later requests reach the same server. Without the session, all three trial logins returned 401.
4. The defect appears when all 3 tools are excluded. HTTP 500 with no body gives a calling app no actionable explanation and treats an unsatisfiable request as a server failure; HTTP 400 with a JSON message would let the app handle it. The strict `xfail` keeps the known defect visible without making the rest of the suite red, and it will fail if the defect is fixed so the marker can be removed.
5. Base choice needs `1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9` tests. All combinations need `3 × 4 × 2 × 3 = 72` tests.
6. The other user's read, update, and delete returned 404, 400, and 400. I would expect a 4xx refusal for each; 403 (forbidden) or a consistent 404 (to hide whether the rating exists) would also be reasonable. They are not defects against this lab's stated 4xx requirement because the other user cannot see or change the rating and the owner still reads the original value. The different 400/404 choices are nevertheless inconsistent API semantics.
7. The made-up 16-character token returned HTTP 200 and a ratings list. Yes, accepting a fabricated token is an authentication defect: a stranger can read shared ratings. I only performed the instructed read and did not try any write operation.
8. An API test checks exact status codes and JSON fields directly and consistently. Only a browser test can check what a person sees and does, such as page layout, rendered errors, and interactive controls.
