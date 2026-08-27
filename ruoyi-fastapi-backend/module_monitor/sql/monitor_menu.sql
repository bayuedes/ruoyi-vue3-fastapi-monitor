-- 监控管理菜单 + 5 个 CRUD 子菜单 + 看板
-- 父菜单: 监控管理 (path=imon)
-- 子菜单: 看板, 资源设备, 监控指标, 子资源类型, 子资源实例, 最新取值
-- 每个子菜单下还有 list/query/add/edit/remove 按钮权限
-- 菜单 ID 从 2000 开始, 避免与现有菜单冲突

USE `ruoyi-fastapi`;

-- 顶级菜单: 监控管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2000, '监控管理', 0, 5, 'imon', NULL, '', '', 1, 0, 'M', '0', '0', '', 'monitor', 'admin', NOW(), 'IT资源监控管理');

-- 看板 (Q1/Q2/Q3 数据展示)
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2001, '监控看板', 2000, 1, 'dashboard', 'imon/dashboard/index', '', '', 1, 0, 'C', '0', '0', 'monitor:dashboard:list', 'dashboard', 'admin', NOW(), '监控统计看板');

-- 资源设备管理 (it_resource_list)
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2010, '资源设备', 2000, 2, 'resource', 'imon/resource/index', '', '', 1, 0, 'C', '0', '0', 'monitor:resource:list', 'server', 'admin', NOW(), '监控资源/设备列表');

INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2011, '资源查询', 2010, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:resource:query', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2012, '资源新增', 2010, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:resource:add', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2013, '资源修改', 2010, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:resource:edit', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2014, '资源删除', 2010, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:resource:remove', '#', 'admin', NOW(), '');

-- 监控指标 (it_resource_index)
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2020, '监控指标', 2000, 3, 'metric', 'imon/metric/index', '', '', 1, 0, 'C', '0', '0', 'monitor:index:list', 'chart', 'admin', NOW(), '监控指标定义');

INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2021, '指标查询', 2020, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:index:query', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2022, '指标新增', 2020, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:index:add', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2023, '指标修改', 2020, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:index:edit', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2024, '指标删除', 2020, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:index:remove', '#', 'admin', NOW(), '');

-- 子资源类型 (it_resource_scan)
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2030, '子资源类型', 2000, 4, 'scan', 'imon/scan/index', '', '', 1, 0, 'C', '0', '0', 'monitor:scan:list', 'cascader', 'admin', NOW(), '子资源类型(磁盘/接口等)');

INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2031, '类型查询', 2030, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scan:query', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2032, '类型新增', 2030, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scan:add', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2033, '类型修改', 2030, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scan:edit', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2034, '类型删除', 2030, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scan:remove', '#', 'admin', NOW(), '');

-- 子资源实例 (it_resource_scaning)
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2040, '子资源实例', 2000, 5, 'scaning', 'imon/scaning/index', '', '', 1, 0, 'C', '0', '0', 'monitor:scaning:list', 'nested', 'admin', NOW(), '资源的子资源实例');

INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2041, '实例查询', 2040, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scaning:query', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2042, '实例新增', 2040, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scaning:add', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2043, '实例修改', 2040, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scaning:edit', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2044, '实例删除', 2040, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:scaning:remove', '#', 'admin', NOW(), '');

-- 最新取值 (it_value_list)
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2050, '最新取值', 2000, 6, 'value', 'imon/value/index', '', '', 1, 0, 'C', '0', '0', 'monitor:value:list', 'list', 'admin', NOW(), '资源最新取值结果');

INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2051, '取值查询', 2050, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:value:query', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2052, '取值新增', 2050, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:value:add', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2053, '取值修改', 2050, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:value:edit', '#', 'admin', NOW(), '');
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (2054, '取值删除', 2050, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'monitor:value:remove', '#', 'admin', NOW(), '');

-- 将所有新增菜单授权给管理员角色 (role_id = 1)
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT 1, menu_id FROM sys_menu WHERE menu_id BETWEEN 2000 AND 2099;
