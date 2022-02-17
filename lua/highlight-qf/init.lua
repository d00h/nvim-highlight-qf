local M = {}

M.state = true
M.virt_text_highlight = 'IncSearch' -- virt_text_pos = 'right_align'
M.virt_text_pos = 'eol'

M.refresh = function()
    local bufnr = vim.fn.bufnr('%')
    local ns_id = vim.api.nvim_create_namespace('quickfix_mark')
    local line_count = vim.api.nvim_buf_line_count(bufnr)
    vim.api.nvim_buf_clear_namespace(bufnr, ns_id, 0, line_count)
    if M.state == true then
        local qflist = vim.fn.getqflist()
        for idx, item in pairs(qflist) do
            if item.bufnr == bufnr then
                local opts = {
                    id = idx,
                    virt_text = {{item.text, M.virt_text_highlight}},
                    virt_text_pos = M.virt_text_pos
                }
                vim.api.nvim_buf_set_extmark(item.bufnr, ns_id, item.lnum - 1,
                                             1, opts)
            end
        end
    end
end

M.set_state = function(new_state)
    if M.state ~= new_state then
        M.state = new_state
        M.refresh()
    end
end

M.run = function(command)
        if command == "refresh" then M.refresh()
    elseif command == "enable" then M.set_state(true)
    elseif command == "disable" then M.set_state(false)
    elseif command == "toggle" then M.set_state(not(M.state))
    else print('refresh|enable|disable|toggle')
    end
end

return M
