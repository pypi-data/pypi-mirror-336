"""
dsef.py

The class containing the algorithms that search and follow edges
"""
import os
import math
import cv2
import numpy as np

from typing import Tuple, Optional, List, Literal

# Import the same modules as your original code
from dsef.dsef_base import DSEFBase
import dsef.dsef_tools as dftools
import dsef.line_tools as linetools

class Dsef:
    """
    Parameters:
        initial_direction_deg (float): The initial direction in degrees.
        direction_span (int): The span of directions for search.
        start_pixel (Tuple[float, float]): Starting pixel (x, y).
        end_pixel (Optional[Tuple[float, float]]): Ending pixel (x, y), optional.
        speed (Literal): Speed of the algorithm, one of "high", "medium", or "low".
        debug (bool): If True, enables debugging prints.
    """
    def __init__(self, 
                 initial_direction_deg: float, 
                 direction_span: int = 90, 
                 start_pixel: Tuple[float, float] = (1, 1), 
                 end_pixel: Optional[Tuple[float, float]] = None, 
                 speed: Literal["high", "medium", "low"] = "medium", 
                 debug=False):
        self.initial_direction_deg = initial_direction_deg
        self.direction_span = direction_span
        self.start_pixel = start_pixel
        self.end_pixel = end_pixel or (None, None)
        self.speed = speed.lower()
        self.debug = debug
        
        self.width = 0
        self.height = 0
        self.E = None

    def edge_search(self, img: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Perform an edge search using the DSEF algorithm.

        Parameters:
            img (np.ndarray): The input image.

        Returns:
            Tuple[bool, np.ndarray]: Whether the edge was found and the resulting image.
        """
        # Image Load and Initialize DSEF
        self._initialize_dsef(img)
        search_step, _ = self._calculate_steps()
        edge_found, image = self._edge_search(search_step, img)

        return edge_found, image


    def edge_follow(self, img: np.ndarray) -> Optional[Tuple[List[Tuple[float, float]],np.ndarray]]:
        """
        Run the DSEF algorithm.

        Parameters:
            img (np.ndarray): The input image.

        Returns:
            Optional[List[Tuple[float, float]]]: List of edge coordinates if found, else None, and resulting image.
        """
        _, follower_step = self._calculate_steps()
        found_edge_line = None
        found_edge_line, image = self._edge_follow(follower_step, img)        
        
        return found_edge_line, image

    @staticmethod
    def convert_image(img: np.ndarray, ORG: bool = False) -> Tuple[np.ndarray,np.ndarray,np.ndarray, Tuple[int,int]]:
        """
        Convert the input image to different color spaces and return processed components.

        Parameters:
            img (np.ndarray): Input image.
            ORG (bool): If True, returns the original RGB image.

        Returns:
            Tuple[np.ndarray, np.ndarray, Optional[np.ndarray], Tuple[int, int]]:
                - The Hue channel of the image.
                - A mask of the image.
                - Original RGB image (if ORG is True).
                - The dimensions of the image (height, width).
        """
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask   = np.ones(im_rgb[:, :, 0].shape, dtype=int)
        im_hsv = cv2.cvtColor(im_rgb, cv2.COLOR_RGB2HSV_FULL)
        if not ORG:
            return im_hsv[:, :, 0], mask, None, im_hsv.shape[:2] # Only Hue and mask
        else:
            return im_hsv[:, :, 0], mask, im_rgb, im_hsv.shape[:2]

    def _initialize_dsef(self, img: np.ndarray) -> None:
        """
        Initialize the DSEF algorithm with the provided image.

        Parameters:
            img (np.ndarray): Input image.
        """
        im_hsv, _, _, (self.height, self.width) = self.convert_image(img, ORG=True)

        self.E = DSEFBase(im_hsv, edge_direction=self.initial_direction_deg, dir_span=self.direction_span, 
                            force_dtheta=self._get_forced_dtheta())

        self.E.DF.flut.reset_span()
        self.E.DF.flut.set_span(self.initial_direction_deg, self.direction_span)

        start_x, start_y = self.start_pixel
        self.E.move(start_x, start_y)

    def _get_forced_dtheta(self) -> float:
        """
        Returns the dtheta adjustment based on speed. 

        Returns:
            float: The dtheta adjustment based on speed.
        """
        speed_mapping = {"high": 10.0, "medium": 4.0, "low": 1.0}
        if self.debug:            
            print("[DEBUG] Overriding d_theta to:", speed_mapping.get(self.speed, 4.0) * self.direction_span / 90)
        return speed_mapping.get(self.speed, 4.0) * self.direction_span / 90

    def _calculate_steps(self) -> Tuple[float, float]:
        """ 
        Calculate search and follower steps based on speed.

        Returns:
            Tuple[float, float]: Search and follower step sizes.
        """
        start_x, start_y = self.start_pixel
        end_x, end_y = self.end_pixel
        dist = math.hypot(end_x - start_x, end_y - start_y)
        diag = math.hypot(self.width, self.height)

        step_mapping = {
            "low": [dist / 20.0/2, diag / 200.0],
            "medium": [dist / 30.0/2, diag / 100.0],
            "high": [dist / 40.0/2, diag / 50.0]
        }
        search_step, follower_step = step_mapping.get(self.speed, [dist / 30.0/2, diag / 100.0])
        if self.debug:
            print("[DEBUG] Distance between start and end:", dist)
            print("[DEBUG] Search step:", search_step)
            print("[DEBUG] Follower step:", follower_step)
        return search_step, follower_step

    def _edge_search(self, search_step: int, img: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Execute the EdgeSearch phase of the algorithm.

        Parameters:
            search_step (int): The search step size.
            img (np.ndarray): The input image.

        Returns:
            Tuple[bool, np.ndarray]: Whether the edge was found and the resulting image.
        """
        start_x, start_y = self.start_pixel
        end_x, end_y = self.end_pixel
        v_dir = [end_x - start_x, end_y - start_y]
        d_ = math.hypot(*v_dir)
        if d_ == 0:
            if self.debug:
                print("[DEBUG] Start and end pixels are the same. Stopping EdgeSearch.")
            return [], []

        v_heading = [v_dir[0] / d_, v_dir[1] / d_]
        MAX_EDGE = 0
        u_edge, v_edge = start_x, start_y
        EDGE_FOUND = False

        while True:
            if not self.E.step(search_step * v_heading[0], search_step * v_heading[1]):
                if self.debug:
                    print("[DEBUG] Step out of image bounds => break EdgeSearch")
                break

            ui, vi = self.E.get_pos()
            image = cv2.circle(img,(int(ui),int(vi)),1,(0,0,0),-1)
            T_FULL_main = dftools.dsef_test(self.E, self.E.u, self.E.v, self.E.edge_direction, FULL=True).FULL or 0
            if T_FULL_main > self.E.crit_edge:
                if T_FULL_main > MAX_EDGE + self.E.crit_edge:
                    MAX_EDGE = T_FULL_main
                    u_edge, v_edge = ui, vi
                    image = cv2.circle(img,(int(u_edge),int(v_edge)),1,(0,0,0),-1)
                elif MAX_EDGE > 0 and T_FULL_main < MAX_EDGE - self.E.crit_edge:
                    self.E.move(u_edge, v_edge)
                    image = cv2.circle(img,(int(u_edge),int(v_edge)),1,(0,0,0),-1)
                    EDGE_FOUND = True
                    if self.debug:
                        print("[DEBUG] Edge found. Breaking EdgeSearch.")
                    break

            v_now = [end_x - ui, end_y - vi]
            if v_heading[0] * v_now[0] + v_heading[1] * v_now[1] <= 0:
                if self.debug:
                    print("[DEBUG] We passed the end pixel => break EdgeSearch.")
                break
        return EDGE_FOUND, image

    def _edge_follow(self, follower_step: int, img: np.ndarray) -> Tuple[List[Tuple[float,float]], np.ndarray]:
        """
        Execute the EdgeFollow phase of the algorithm.

        Parameters:
            follower_step (int): The follower step size.
            img (np.ndarray): The input image.

        Returns:
            Tuple[List[Tuple[float, float]], np.ndarray]: The found edge line and the resulting image.
        """
        found_edge_line = []
        
        EDGE_FOUND, _, REWA, message, us, vs, arrow_list_follow, image = self.E.EdgeFollow(follower_step, img)
        
        if self.debug and message:
            print("[DEBUG] EdgeFollow message:", message)

        if EDGE_FOUND:
            x_start = self.E.u_edge
            y_start = self.E.v_edge
            direction_vec = REWA.mu
            # Draw a big line for visualization
            x_end = x_start + 1000*follower_step * direction_vec[0]
            y_end = y_start + 1000*follower_step * direction_vec[1]
            found_edge_line = [(x_start, y_start), (x_end, y_end)]
            
        return found_edge_line, image

        """ Patched EdgeFollow method using follower_step. 

        Parameters:
            follower_step (int): The follower step size.
            img (np.ndarray): The input image.
            MAX_ITT (int): maximum number of iterations.
            Ntest_edge (int): number of tests for considering an edge

        Returns:
            Tuple[List[Tuple[float, float]], np.ndarray]: The found edge line and the resulting image.
        """
        print(self)
        step = follower_step
        sel_dirs, _, sel_dirvecs = self.E.DF.flut.get_span()
        consec_edge, consec_no_edge = 0, 0
        message = None
        self.E.u_edge, self.E.v_edge = self.E.get_pos()
        EDGE_FOUND, END_FOUND = False, False
        ABORT_WHEN_ACCURATE = True 
        REWA = linetools.RunningExponentialVectorAverage(var=np.array([2,2]), rho=0.1)

        # pick best direction from current span
        t1 = [dftools.dsef_test(self.E, self.E.u, self.E.v, d, FORWARD=True, FULL=True).FULL for d in sel_dirs]
        ind_max = np.argmax(t1)
        best_direction = sel_dirvecs[ind_max]
        REWA.push(best_direction)

        us_, vs_ = [], []
        arrow_list_follow = []  # We'll store arrow info for each iteration
        Nitt = 0

        while Nitt < MAX_ITT:
            Nitt += 1
            ui, vi = self.E.get_pos()
            image = cv2.circle(img,(int(ui),int(vi)),1,(128,128,128),-1)
            us_.append(ui)
            vs_.append(vi)

            # forward test for each direction
            t_ = [dftools.dsef_test(self.E, self.E.u, self.E.v, d, FORWARD=True, FULL=True).FULL for d in sel_dirs]
            ind_max = np.argmax(t_)
            if t_[ind_max] < t_[len(sel_dirs)//2] + self.E.crit_edge:
                ind_max = len(sel_dirs)//2
            v = sel_dirvecs[ind_max]
            T_ALL = dftools.dsef_test(self.E, self.E.u, self.E.v, sel_dirs[ind_max], ALL=True).ALL
            if T_ALL is None:
                T_ALL = []
            ALL_EDGE = np.all(np.array(T_ALL) > self.E.crit_edge)

            # e.g. store direction & T_FORWARD in arrow_list_follow
            arrow_list_follow.append([
                (d, t_val if t_val is not None else 0.0)
                for d, t_val in zip(sel_dirs, t_)
            ])

            if ALL_EDGE:
                consec_edge = min(consec_edge+1, Ntest_edge)
                consec_no_edge = 0
            else:
                consec_edge = max(0, consec_edge-1)
                consec_no_edge += 1

            if consec_no_edge >= 2*self.E.DF.N + 1:
                message = "CANCEL. WE LOST THE EDGE"
                break

            if consec_edge >= Ntest_edge:
                if not EDGE_FOUND:
                    self.E.u_edge, self.E.v_edge = self.E.get_pos()
                    EDGE_FOUND = True
                REWA.push(v)
                mu_direction = self.E.DF.flut.wrap_angle(linetools.calc_heading(REWA.mu))
                var_direction = REWA.var[0]**2 
                var_direction = np.degrees(np.arctan(REWA.var[1]/(1+REWA.var[0])))

                if var_direction > self.E.DF.flut.d_theta:
                    self.E.DF.flut.set_span(mu_direction, 4*var_direction**0.5)
                    sel_dirs, sel_items, sel_dirvecs = self.E.DF.flut.get_span()
                elif ABORT_WHEN_ACCURATE:
                    message = ("ABORTING. Edge direction +/- %.1f deg" 
                                % (var_direction**0.5))
                    break

            # move filter forward
            if not self.E.step(v[0]*step, v[1]*step):
                message = "we reached END of image"
                break

        return EDGE_FOUND, END_FOUND, REWA, message, us_, vs_, arrow_list_follow, image