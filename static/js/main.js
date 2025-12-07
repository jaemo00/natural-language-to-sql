// -------- users 전체 조회 --------
const usersBox = document.getElementById("users-box");
const refreshUsersBtn = document.getElementById("refresh-users-btn");
const ordersBox = document.getElementById("orders-box");
const refreshOrdersBtn = document.getElementById("refresh-orders-btn");

async function loadUsers() {
    usersBox.textContent = "로딩 중...";
    try {
        const res = await fetch("/api/users");
        if (!res.ok) {
            const text = await res.text();
            usersBox.textContent = "에러: " + res.status + "\n" + text;
            return;
        }
        const data = await res.json();
        const rows = data.rows || [];

        if (rows.length === 0) {
            usersBox.textContent = "(데이터 없음)";
            return;
        }

        const keys = Object.keys(rows[0]);
        let html = "<table><thead><tr>";

        // 기존 컬럼 헤더
        for (const k of keys) {
            html += "<th>" + k + "</th>";
        }
     
        html += "<th>삭제</th>";

        html += "</tr></thead><tbody>";

        for (const row of rows) {
            html += "<tr>";
            // 기존 컬럼 값들
            for (const k of keys) {
                let v = row[k];
                if (v === null || v === undefined) v = "";
                html += "<td>" + v + "</td>";
            }
    
            html += `<td>
                <button class="btn ghost" onclick="deleteUser(${row.id})">
                    삭제
                </button>
            </td>`;
            html += "</tr>";
        }

        html += "</tbody></table>";
        usersBox.innerHTML = html;
    } catch (err) {
        usersBox.textContent = "로딩 실패: " + err;
    }
}
async function loadOrders() {
    ordersBox.textContent = "로딩 중...";
    try {
        const res = await fetch("/api/orders");
        if (!res.ok) {
            const text = await res.text();
            ordersBox.textContent = "에러: " + res.status + "\n" + text;
            return;
        }
        const data = await res.json();
        const rows = data.rows || [];

        if (rows.length === 0) {
            ordersBox.textContent = "(데이터 없음)";
            return;
        }

        const keys = Object.keys(rows[0]);
        let html = "<table><thead><tr>";

        for (const k of keys) {
            html += "<th>" + k + "</th>";
        }
        // ✅ 마지막에 삭제 버튼 컬럼
        html += "<th>삭제</th>";

        html += "</tr></thead><tbody>";

        for (const row of rows) {
            html += "<tr>";
            for (const k of keys) {
                let v = row[k];
                if (v === null || v === undefined) v = "";
                html += "<td>" + v + "</td>";
            }
            html += `<td>
                <button class="btn ghost" onclick="deleteOrder(${row.id})">
                    삭제
                </button>
            </td>`;
            html += "</tr>";
        }

        html += "</tbody></table>";
        ordersBox.innerHTML = html;
    } catch (err) {
        ordersBox.textContent = "로딩 실패: " + err;
    }
}

refreshOrdersBtn.addEventListener("click", loadOrders);
loadOrders();
refreshUsersBtn.addEventListener("click", loadUsers);
loadUsers();


// -------- users 추가 폼 --------
const addUserForm = document.getElementById("add-user-form");
const addUserMsg = document.getElementById("add-user-message");

addUserForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    addUserMsg.textContent = "";

    const formData = new FormData(addUserForm);
    const payload = {
        name: formData.get("name") || "",
        age: formData.get("age") ? Number(formData.get("age")) : null,
        city: formData.get("city") || null,
    };

    try {
        const res = await fetch("/api/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await res.json();

        if (!res.ok) {
            addUserMsg.textContent = "추가 실패: " + (data.error || res.status);
            return;
        }

        addUserMsg.textContent = "추가 완료! (id=" + data.id + ")";
        addUserForm.reset();
        loadUsers();
    } catch (err) {
        addUserMsg.textContent = "요청 중 에러: " + err;
    }
});


// -------- NL -> SQL 테스트 폼 --------
const form = document.getElementById("query-form");
const sqlBox = document.getElementById("sql-box");
const rowsBox = document.getElementById("rows-box");



form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const payload = {
        table: formData.get("table") || "",
        columns: formData.get("columns") || "",
        conditions: formData.get("conditions") || ""
    };

    sqlBox.textContent = "요청 중...";
    rowsBox.textContent = "";

    try {
        const res = await fetch("/api/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            const text = await res.text();
            sqlBox.textContent = "에러: " + res.status + "\n" + text;
            rowsBox.textContent = "";
            return;
        }

        const data = await res.json();
        sqlBox.textContent = data.sql || "(SQL 없음)";

        const rows = data.rows || [];
        if (rows.length === 0) {
            rowsBox.textContent = "(결과 없음)";
        } else {
            const keys = Object.keys(rows[0]);

            let html = "<table><thead><tr>";
            for (const k of keys) {
                html += "<th>" + k + "</th>";
            }
            html += "</tr></thead><tbody>";

            for (const row of rows) {
                html += "<tr>";
                for (const k of keys) {
                    let value = row[k];
                    if (value === null || value === undefined) {
                        value = "";
                    }
                    html += "<td>" + value + "</td>";
                }
                html += "</tr>";
            }

            html += "</tbody></table>";
            rowsBox.innerHTML = html;
        }
    } catch (err) {
        sqlBox.textContent = "요청 중 에러 발생: " + err;
        rowsBox.textContent = "";
    }
});
async function deleteUser(id) {
    const sure = confirm(`정말로 ID ${id} 사용자를 삭제할까요?`);
    if (!sure) return;

    try {
        const res = await fetch(`/api/users/${id}`, {
            method: "DELETE",
        });

        let data = {};
        try {
            data = await res.json();
        } catch (_) {
            // body가 없거나 JSON 아니어도 그냥 무시
        }

        if (!res.ok) {
            alert("삭제 실패: " + (data.error || res.status));
            return;
        }

        // 삭제 성공 → 목록 갱신
        loadUsers();
    } catch (err) {
        alert("요청 중 에러: " + err);
    }
}

async function deleteOrder(id) {
    const sure = confirm(`정말로 주문 ID ${id}를 삭제할까요?`);
    if (!sure) return;

    try {
        const res = await fetch(`/api/orders/${id}`, {
            method: "DELETE",
        });

        let data = {};
        try {
            data = await res.json();
        } catch (_) {
            // body 없으면 무시
        }

        if (!res.ok) {
            alert("삭제 실패: " + (data.error || res.status));
            return;
        }

        // orders 갱신
        loadOrders();
    } catch (err) {
        alert("요청 중 에러: " + err);
    }
}

// -------- LLM 기반 NL → SQL --------
const nl2sqlForm = document.getElementById("nl2sql-form");
const nl2sqlSqlBox = document.getElementById("nl2sql-sql-box");
const nl2sqlRowsBox = document.getElementById("nl2sql-rows-box");

if (nl2sqlForm) {
    nl2sqlForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(nl2sqlForm);
        const message = formData.get("message") || "";

        if (!message.trim()) {
            nl2sqlSqlBox.textContent = "(문장을 입력해주세요)";
            nl2sqlRowsBox.textContent = "";
            return;
        }

        nl2sqlSqlBox.textContent = "LLM 호출 중...";
        nl2sqlRowsBox.textContent = "";

        try {
            const res = await fetch("/api/nl2sql", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });

            const data = await res.json();

            if (!res.ok) {
                nl2sqlSqlBox.textContent = "에러: " + (data.error || res.status);
                nl2sqlRowsBox.textContent = "";
                return;
            }

            nl2sqlSqlBox.textContent = data.sql || "(SQL 없음)";

            const rows = data.rows || [];
            if (rows.length === 0) {
                nl2sqlRowsBox.textContent = "(결과 없음)";
            } else {
                const keys = Object.keys(rows[0]);
                let html = "<table><thead><tr>";
                for (const k of keys) {
                    html += "<th>" + k + "</th>";
                }
                html += "</tr></thead><tbody>";

                for (const row of rows) {
                    html += "<tr>";
                    for (const k of keys) {
                        let v = row[k];
                        if (v === null || v === undefined) v = "";
                        html += "<td>" + v + "</td>";
                    }
                    html += "</tr>";
                }
                html += "</tbody></table>";
                nl2sqlRowsBox.innerHTML = html;
            }
        } catch (err) {
            nl2sqlSqlBox.textContent = "요청 중 에러: " + err;
            nl2sqlRowsBox.textContent = "";
        }
    });
}

// ====== 주문 추가 기능 ======
const addOrderForm = document.getElementById("add-order-form");
const addOrderMessage = document.getElementById("add-order-message");

if (addOrderForm) {
    addOrderForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(addOrderForm);
        const body = {};
        formData.forEach((v, k) => (body[k] = v));

        addOrderMessage.textContent = "추가 중...";

        try {
            const res = await fetch("/api/orders", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            let data = {};
            try {
                data = await res.json();
            } catch (_) {}

            if (!res.ok) {
                addOrderMessage.textContent =
                    "에러: " + (data.error || res.status);
                return;
            }

            addOrderMessage.textContent = "추가 완료!";

            // 🔄 orders 테이블 갱신
            if (typeof loadOrders === "function") {
                loadOrders();
            }
        } catch (err) {
            addOrderMessage.textContent = "요청 실패: " + err;
        }

        // 입력창 초기화
        addOrderForm.reset();
    });
}

