export type VNode = VNodeWithoutData | VNodeWithData;
export type VNodeWithoutData = [string, ...VNodeChild[]];
export type VNodeWithData = [string, VNodeData, ...VNodeChild[]];
export type VNodeData = Record<string, any>;
export type VNodeChild = string | VNode | VNodeChild[];
export type VNodePath = number | VNodePath[];
export declare function isVNodeWithoutData(node: VNode): node is VNodeWithoutData;
export declare function isVNodeWithData(node: VNode): node is VNodeWithData;
export declare function isVNode(child: VNodeChild): child is VNode;
export declare function getVNodeChildren(node: VNode): VNodeChild[];
export declare function getFlatVNodeChildren(node: VNode): (string | VNode)[];
export declare function flattenVNodeChildren(children: VNodeChild[]): Generator<string | VNode>;
export declare function _changeVNodeData(fn: (data: VNodeData | null) => VNodeData | null, node: VNode): VNode;
export declare const changeVNodeData: import("./curry.js").Curried2<(data: VNodeData | null) => VNodeData | null, VNode, VNode>;
export declare function _changeVNodeChildren(fn: (children: VNodeChild[]) => VNodeChild[], node: VNode): VNode;
export declare const changeVNodeChildren: import("./curry.js").Curried2<(children: VNodeChild[]) => VNodeChild[], VNode, VNode>;
export declare function _queryVNodePath(selector: string, tree: VNodeChild): VNodePath | null;
export declare const queryVNodePath: import("./curry.js").Curried2<string, VNodeChild, VNodePath | null>;
export declare function _queryAllVNodePaths(selector: string, tree: VNodeChild): Generator<VNodePath>;
export declare const queryAllVNodePaths: import("./curry.js").Curried2<string, VNodeChild, Generator<VNodePath, any, unknown>>;
export declare function _getVNode(path: VNodePath, tree: VNodeChild): VNode | null;
export declare const getVNode: import("./curry.js").Curried2<VNodePath, VNodeChild, VNode | null>;
export declare function _changeVNode(path: VNodePath, fn: (val: VNode) => VNode, tree: VNodeChild): VNodeChild;
export declare const changeVNode: import("./curry.js").Curried3<VNodePath, (val: VNode) => VNode, VNodeChild, VNodeChild>;
export declare function _setVNode(path: VNodePath, node: VNode, tree: VNodeChild): VNodeChild;
export declare const setVNode: import("./curry.js").Curried3<VNodePath, VNode, VNodeChild, VNodeChild>;
export declare function _omitVNode(path: VNodePath, tree: VNodeChild): VNodeChild;
export declare const omitVNode: import("./curry.js").Curried2<VNodePath, VNodeChild, VNodeChild>;
